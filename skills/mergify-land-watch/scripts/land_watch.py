#!/usr/bin/env python3
"""Wait until a pull request is merge-ready, queue it with Mergify, and follow the queue until it merges.

The watcher acts only on states it recognizes. Anything else ends the run with a reason, so the agent that started
it can review the pull request and start it again.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Callable

EXIT_MERGED = 0
EXIT_ERROR = 1
EXIT_USAGE = 2
EXIT_ATTENTION = 3
EXIT_TIMEOUT = 4

QUEUE_COMMENT = "@mergifyio queue"
PAYLOAD_RE = re.compile(r"-\*- Mergify Payload -\*-\s*(\{.*?\})\s*-\*- Mergify Payload End -\*-", re.S)
PR_URL_RE = re.compile(r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<number>\d+)/?$")
OK_CHECK_STATES = {"SUCCESS", "SKIPPED"}
PENDING_CHECK_STATES = {"PENDING", "QUEUED", "IN_PROGRESS", "WAITING", "REQUESTED", "EXPECTED"}
# A check that registers late can look like "nothing pending", so the ready state must hold on two reads.
READY_READS = 2
# Mergify can update its status comment a moment before GitHub reports the merge.
NON_CHECKING_READS = 2
MAX_CONSECUTIVE_ERRORS = 5


class GhError(RuntimeError):
    pass


@dataclass
class Snapshot:
    state: str
    is_draft: bool
    head: str
    base: str
    default_branch: str
    labels: list[str]
    merge_state: str
    review_decision: str
    reviews: list[dict]
    checks: list[dict]
    unresolved_threads: int
    new_comments: list[dict]
    mergify: dict | None
    edited_comments: list[dict] = field(default_factory=list)
    merge_commit: str | None = None
    merged_at: str | None = None


@dataclass
class Options:
    head: str
    required_checks: list[str]
    one_of_labels: list[str]
    ignore_check: re.Pattern | None
    ignore_commenter: re.Pattern | None


@dataclass
class Verdict:
    kind: str
    reasons: list[str] = field(default_factory=list)


def evaluate_ready(s: Snapshot, o: Options) -> Verdict:
    attention: list[str] = []
    wait: list[str] = []

    if s.state != "OPEN":
        attention.append(f"pull request is {s.state.lower()}")
    if s.head != o.head:
        attention.append(f"head moved from {o.head[:10]} to {s.head[:10]}")
    if s.is_draft:
        attention.append("pull request is a draft")
    if s.base != s.default_branch:
        attention.append(f"base is {s.base}, not {s.default_branch}: a stack needs the top pull request procedure")
    if o.one_of_labels:
        present = [label for label in o.one_of_labels if label in s.labels]
        if len(present) != 1:
            attention.append(f"needs exactly one of {', '.join(o.one_of_labels)}, has {', '.join(present) or 'none'}")
    if s.merge_state == "DIRTY":
        attention.append("merge conflict with the base branch")

    for check in s.checks:
        if o.ignore_check and o.ignore_check.search(check["name"]):
            continue
        if check["state"] in OK_CHECK_STATES:
            continue
        if check["state"] in PENDING_CHECK_STATES:
            wait.append(f"check {check['name']} is {check['state'].lower()}")
            continue
        # An AI reviewer reports a finding as a neutral conclusion, so every other state needs a reader.
        attention.append(f"check {check['name']} ended {check['state'].lower()}")
    succeeded = {check["name"] for check in s.checks if check["state"] == "SUCCESS"}
    for name in o.required_checks:
        if name not in succeeded:
            wait.append(f"required check {name} has not succeeded")

    blocking = [review["login"] for review in s.reviews if review["state"] == "CHANGES_REQUESTED"]
    if blocking or s.review_decision == "CHANGES_REQUESTED":
        attention.append(f"changes requested by {', '.join(blocking) or 'a reviewer'}")
    eligible = [review for review in s.reviews if review["state"] == "APPROVED" and review["can_push"]]
    if not any(review["commit"] == o.head for review in eligible):
        if eligible:
            wait.append("the eligible approval is on an older commit")
        else:
            wait.append("no eligible approval yet")
    if s.review_decision == "REVIEW_REQUIRED":
        wait.append("GitHub still requires a review")

    if s.unresolved_threads:
        attention.append(f"{s.unresolved_threads} unresolved review thread(s)")
    for comment in s.new_comments:
        if o.ignore_commenter and o.ignore_commenter.search(comment["login"]):
            continue
        attention.append(f"new {comment['kind']} from {comment['login']}")

    if attention:
        return Verdict("attention", attention)
    if wait:
        return Verdict("wait", wait)
    # A summary bot fills its findings in by editing one comment, so an edit since the start blocks the queue. The
    # check runs only at the ready moment, because summary comments are edited many times while reviews run.
    for comment in s.edited_comments:
        if o.ignore_commenter and o.ignore_commenter.search(comment["login"]):
            continue
        attention.append(f"comment from {comment['login']} was edited after the start; read it")

    if attention:
        return Verdict("attention", attention)
    return Verdict("ready")


def parse_mergify_payload(comments: list[dict]) -> dict | None:
    latest = None
    for comment in comments:
        if "mergify" not in comment["login"].lower():
            continue
        match = PAYLOAD_RE.search(comment["body"] or "")
        if not match:
            continue
        try:
            payload = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        if latest is None or comment["updated_at"] > latest[0]:
            latest = (comment["updated_at"], payload)
    return latest[1] if latest else None


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def gh(args: list[str], allow_failure: bool = False) -> str:
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0 and not allow_failure:
        raise GhError(f"gh {' '.join(args[:3])} failed: {result.stderr.strip()[:300]}")
    return result.stdout


def json_lines(output: str) -> list:
    return [json.loads(line) for line in output.splitlines() if line.strip()]


PR_QUERY = """
query($owner:String!,$repo:String!,$number:Int!){repository(owner:$owner,name:$repo){
  defaultBranchRef{name}
  pullRequest(number:$number){state isDraft headRefOid baseRefName mergeStateStatus reviewDecision mergedAt
    mergeCommit{oid} labels(first:100){nodes{name}}
    latestOpinionatedReviews(first:100){nodes{state authorCanPushToRepository author{login} commit{oid}}}}}}
"""
THREADS_QUERY = """
query($owner:String!,$repo:String!,$number:Int!,$endCursor:String){repository(owner:$owner,name:$repo){
  pullRequest(number:$number){reviewThreads(first:100,after:$endCursor){nodes{isResolved}
    pageInfo{hasNextPage endCursor}}}}}
"""


@dataclass
class PullRequest:
    owner: str
    repo: str
    number: int

    @property
    def url(self) -> str:
        return f"https://github.com/{self.owner}/{self.repo}/pull/{self.number}"


def fetch_snapshot(pr: PullRequest, since: datetime, own_comment_ids: set[int]) -> Snapshot:
    variables = ["-F", f"owner={pr.owner}", "-F", f"repo={pr.repo}", "-F", f"number={pr.number}"]
    data = json.loads(gh(["api", "graphql", "-f", f"query={PR_QUERY}", *variables]))["data"]["repository"]
    node = data["pullRequest"]
    threads = gh(
        ["api", "graphql", "--paginate", "-f", f"query={THREADS_QUERY}", *variables,
         "--jq", ".data.repository.pullRequest.reviewThreads.nodes[].isResolved"]
    ).split()
    # `gh pr checks` exits non-zero while a check is pending or failed, and still prints the JSON.
    raw_checks = gh(["pr", "checks", pr.url, "--json", "name,state"], allow_failure=True).strip()
    checks = json.loads(raw_checks) if raw_checks.startswith("[") else []
    comments = [
        {"id": row[0], "login": row[1], "created_at": row[2], "updated_at": row[3], "body": row[4]}
        for row in json_lines(gh(["api", "--paginate", f"repos/{pr.owner}/{pr.repo}/issues/{pr.number}/comments",
                                  "--jq", ".[] | [.id, .user.login, .created_at, .updated_at, .body] | @json"]))
    ]
    reviews = json_lines(gh(["api", "--paginate", f"repos/{pr.owner}/{pr.repo}/pulls/{pr.number}/reviews",
                             "--jq", ".[] | [.id, .user.login, .state, .submitted_at, .body] | @json"]))

    new_comments = [
        {"login": c["login"], "kind": "comment"}
        for c in comments
        if c["id"] not in own_comment_ids and parse_time(c["created_at"]) > since
    ]
    new_comments += [
        {"login": r[1], "kind": "review comment"}
        for r in reviews
        if r[2] == "COMMENTED" and (r[4] or "").strip() and r[3] and parse_time(r[3]) > since
    ]
    edited_comments = [
        {"login": c["login"]}
        for c in comments
        if c["id"] not in own_comment_ids
        and not PAYLOAD_RE.search(c["body"] or "")
        and parse_time(c["created_at"]) <= since
        and parse_time(c["updated_at"]) > since
    ]
    return Snapshot(
        state=node["state"],
        is_draft=node["isDraft"],
        head=node["headRefOid"],
        base=node["baseRefName"],
        default_branch=data["defaultBranchRef"]["name"],
        labels=[label["name"] for label in node["labels"]["nodes"]],
        merge_state=node["mergeStateStatus"] or "",
        review_decision=node["reviewDecision"] or "",
        reviews=[
            {"state": r["state"], "login": (r["author"] or {}).get("login", ""),
             "can_push": bool(r["authorCanPushToRepository"]), "commit": (r["commit"] or {}).get("oid", "")}
            for r in node["latestOpinionatedReviews"]["nodes"]
        ],
        checks=checks,
        unresolved_threads=threads.count("false"),
        new_comments=new_comments,
        mergify=parse_mergify_payload(comments),
        edited_comments=edited_comments,
        merge_commit=(node["mergeCommit"] or {}).get("oid"),
        merged_at=node["mergedAt"],
    )


def post_queue_comment(pr: PullRequest) -> tuple[int, str]:
    row = json.loads(gh(["api", f"repos/{pr.owner}/{pr.repo}/issues/{pr.number}/comments",
                         "-f", f"body={QUEUE_COMMENT}", "--jq", "[.id, .created_at] | @json"]))
    return row[0], row[1]


@dataclass
class Result:
    code: int
    result: str
    reasons: list[str] = field(default_factory=list)
    extra: dict = field(default_factory=dict)


class Watcher:
    def __init__(
        self,
        pr: PullRequest,
        options: Options,
        *,
        interval: float,
        timeout: timedelta,
        ack_timeout: timedelta,
        dry_run: bool,
        fetch: Callable[[PullRequest, datetime, set[int]], Snapshot] = fetch_snapshot,
        post: Callable[[PullRequest], tuple[int, str]] = post_queue_comment,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
        sleep: Callable[[float], None] = time.sleep,
        log: Callable[[str], None] = lambda line: print(line, flush=True),
    ):
        self.pr, self.options = pr, options
        self.interval, self.timeout, self.ack_timeout, self.dry_run = interval, timeout, ack_timeout, dry_run
        self.fetch, self.post, self.now, self.sleep, self.log = fetch, post, now, sleep, log
        self.own_comment_ids: set[int] = set()
        self.last_status = ""

    def status(self, line: str) -> None:
        if line != self.last_status:
            self.log(f"{self.now():%H:%M:%S} {line}")
            self.last_status = line

    def run(self) -> Result:
        start = self.now()
        deadline = start + self.timeout
        phase, ready_reads, non_checking_reads, errors = "ready", 0, 0, 0
        posted_at: datetime | None = None
        while self.now() < deadline:
            try:
                s = self.fetch(self.pr, start, self.own_comment_ids)
                errors = 0
            except (GhError, json.JSONDecodeError, KeyError, TypeError) as error:
                errors += 1
                self.status(f"read failed ({errors}/{MAX_CONSECUTIVE_ERRORS}): {error}")
                if errors >= MAX_CONSECUTIVE_ERRORS:
                    return Result(EXIT_ERROR, "error", [str(error)])
                self.sleep(self.interval)
                continue

            if s.state == "MERGED":
                return Result(EXIT_MERGED, "merged", extra={"merge_commit": s.merge_commit, "merged_at": s.merged_at})
            payload_state = (s.mergify or {}).get("state")

            if phase == "ready":
                if payload_state == "checking" and (s.mergify or {}).get("queued_at"):
                    if self.dry_run:
                        return Result(EXIT_MERGED, "dry-run", ["already in the Mergify queue"])
                    phase = "queued"
                    self.status("already in the Mergify queue")
                else:
                    verdict = evaluate_ready(s, self.options)
                    if verdict.kind == "attention":
                        return Result(EXIT_ATTENTION, "attention", verdict.reasons)
                    ready_reads = ready_reads + 1 if verdict.kind == "ready" else 0
                    self.status("ready" if verdict.kind == "ready" else f"waiting: {verdict.reasons[0]}")
                    if self.dry_run:
                        would = "would queue" if verdict.kind == "ready" else "would wait"
                        return Result(EXIT_MERGED, "dry-run", [would, *verdict.reasons])
                    if ready_reads >= READY_READS:
                        comment_id, created_at = self.post(self.pr)
                        self.own_comment_ids.add(comment_id)
                        posted_at = parse_time(created_at)
                        phase = "acknowledging"
                        self.status(f"posted {QUEUE_COMMENT}")
            elif phase == "acknowledging":
                queued_at = (s.mergify or {}).get("queued_at")
                if payload_state == "checking" and queued_at and posted_at and parse_time(queued_at) >= posted_at - timedelta(seconds=60):
                    phase = "queued"
                    self.status("Mergify queued the pull request")
                elif posted_at and self.now() > posted_at + self.ack_timeout:
                    return Result(EXIT_ATTENTION, "attention",
                                  [f"Mergify did not acknowledge {QUEUE_COMMENT}; read its reply on the pull request"])
            if phase == "queued":
                if s.state == "CLOSED":
                    return Result(EXIT_ATTENTION, "attention", ["pull request closed while queued"])
                if s.head != self.options.head:
                    return Result(EXIT_ATTENTION, "attention", [f"head moved to {s.head[:10]} while queued"])
                if payload_state == "merged":
                    # Mergify reports the merge a moment before GitHub does, so wait for the pull request state.
                    self.status("Mergify reports the merge, waiting for GitHub")
                elif payload_state != "checking":
                    non_checking_reads += 1
                    if non_checking_reads >= NON_CHECKING_READS:
                        return Result(EXIT_ATTENTION, "attention", [f"Mergify queue state is {payload_state or 'missing'}"])
                else:
                    non_checking_reads = 0
                    step = (s.mergify or {}).get("step", "")
                    self.status(f"queued: {step}" if step else "queued")
            self.sleep(self.interval)
        return Result(EXIT_TIMEOUT, "timeout", [f"no merge within {self.timeout}"])


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pr_url", help="https://github.com/OWNER/REPO/pull/NUMBER")
    parser.add_argument("--head", required=True, help="the head SHA the agent reviewed; the watcher queues only this head")
    parser.add_argument("--required-check", action="append", default=[], dest="required_checks",
                        help="a check that must succeed before queueing; repeat for more")
    parser.add_argument("--one-of-label", default="", help="comma-separated labels, of which exactly one must be set")
    parser.add_argument("--ignore-check", default=r"^Mergify ", help="regex of check names to ignore")
    parser.add_argument("--ignore-commenter", default="", help="regex of logins whose new comments do not stop the run")
    parser.add_argument("--interval", type=float, default=60, help="seconds between reads")
    parser.add_argument("--timeout-hours", type=float, default=6)
    parser.add_argument("--ack-timeout-minutes", type=float, default=5)
    parser.add_argument("--dry-run", action="store_true", help="read once, print the verdict, and post nothing")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    match = PR_URL_RE.match(args.pr_url)
    if not match or not re.fullmatch(r"[0-9a-f]{40}", args.head):
        print("expected a pull request URL and a full 40-character --head SHA", file=sys.stderr)
        return EXIT_USAGE
    if not args.required_checks:
        print("pass at least one --required-check, so an empty check list never reads as green", file=sys.stderr)
        return EXIT_USAGE
    options = Options(
        head=args.head,
        required_checks=args.required_checks,
        one_of_labels=[label for label in args.one_of_label.split(",") if label],
        ignore_check=re.compile(args.ignore_check) if args.ignore_check else None,
        ignore_commenter=re.compile(args.ignore_commenter) if args.ignore_commenter else None,
    )
    watcher = Watcher(
        PullRequest(match["owner"], match["repo"], int(match["number"])),
        options,
        interval=args.interval,
        timeout=timedelta(hours=args.timeout_hours),
        ack_timeout=timedelta(minutes=args.ack_timeout_minutes),
        dry_run=args.dry_run,
    )
    result = watcher.run()
    print("RESULT " + json.dumps({"result": result.result, "reasons": result.reasons, **result.extra}), flush=True)
    return result.code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
