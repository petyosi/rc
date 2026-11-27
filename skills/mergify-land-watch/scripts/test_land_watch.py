from __future__ import annotations

import re
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone

from land_watch import (
    EXIT_ATTENTION,
    EXIT_MERGED,
    EXIT_TIMEOUT,
    Options,
    PullRequest,
    Snapshot,
    Watcher,
    evaluate_ready,
    parse_mergify_payload,
)

HEAD = "a" * 40
OLD = "b" * 40
START = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)


def payload_comment(state: str, queued_at: str | None, updated_at: str = "2030-01-01T12:05:00Z", extra: str = "") -> dict:
    fields = f'"state": "{state}"' + (f', "queued_at": "{queued_at}"' if queued_at else "")
    body = f"<!--\n-*- Mergify Payload -*-\n{{{fields}{extra}}}\n-*- Mergify Payload End -*-\n-->\nstatus"
    return {"login": "mergify[bot]", "body": body, "updated_at": updated_at}


def snapshot(**changes) -> Snapshot:
    base = Snapshot(
        state="OPEN",
        is_draft=False,
        head=HEAD,
        base="main",
        default_branch="main",
        labels=["safe-to-revert"],
        merge_state="BLOCKED",
        review_decision="",
        reviews=[{"state": "APPROVED", "login": "review-bot", "can_push": True, "commit": HEAD}],
        checks=[
            {"name": "aggregate", "state": "SUCCESS"},
            {"name": "lint", "state": "SKIPPED"},
            {"name": "Mergify Merge Protections", "state": "NEUTRAL"},
        ],
        unresolved_threads=0,
        new_comments=[],
        mergify=None,
    )
    return replace(base, **changes)


OPTIONS = Options(
    head=HEAD,
    required_checks=["aggregate"],
    one_of_labels=["safe-to-revert", "unsafe-to-revert"],
    ignore_check=re.compile(r"^Mergify "),
    ignore_commenter=re.compile(r"^ci-bot$"),
)


class EvaluateReadyTests(unittest.TestCase):
    def test_ready_with_bot_approval_and_empty_review_decision(self):
        self.assertEqual(evaluate_ready(snapshot(), OPTIONS).kind, "ready")

    def test_waits_while_no_check_has_registered(self):
        verdict = evaluate_ready(snapshot(checks=[]), OPTIONS)
        self.assertEqual(verdict.kind, "wait")
        self.assertIn("required check aggregate has not succeeded", verdict.reasons)

    def test_waits_on_pending_check(self):
        checks = [{"name": "aggregate", "state": "SUCCESS"}, {"name": "review", "state": "IN_PROGRESS"}]
        self.assertEqual(evaluate_ready(snapshot(checks=checks), OPTIONS).kind, "wait")

    def test_neutral_check_outside_the_ignore_list_needs_attention(self):
        checks = [{"name": "aggregate", "state": "SUCCESS"}, {"name": "AI review", "state": "NEUTRAL"}]
        verdict = evaluate_ready(snapshot(checks=checks), OPTIONS)
        self.assertEqual(verdict.kind, "attention")
        self.assertIn("check AI review ended neutral", verdict.reasons)

    def test_unknown_check_state_needs_attention(self):
        checks = [{"name": "aggregate", "state": "SUCCESS"}, {"name": "build", "state": "STARTUP_FAILURE"}]
        self.assertEqual(evaluate_ready(snapshot(checks=checks), OPTIONS).kind, "attention")

    def test_approval_on_older_commit_waits(self):
        reviews = [{"state": "APPROVED", "login": "review-bot", "can_push": True, "commit": OLD}]
        verdict = evaluate_ready(snapshot(reviews=reviews), OPTIONS)
        self.assertEqual(verdict.kind, "wait")
        self.assertIn("the eligible approval is on an older commit", verdict.reasons)

    def test_approval_without_push_access_does_not_count(self):
        reviews = [{"state": "APPROVED", "login": "outsider", "can_push": False, "commit": HEAD}]
        self.assertEqual(evaluate_ready(snapshot(reviews=reviews), OPTIONS).reasons, ["no eligible approval yet"])

    def test_changes_request_needs_attention(self):
        reviews = [
            {"state": "APPROVED", "login": "review-bot", "can_push": True, "commit": HEAD},
            {"state": "CHANGES_REQUESTED", "login": "person", "can_push": True, "commit": HEAD},
        ]
        self.assertEqual(evaluate_ready(snapshot(reviews=reviews), OPTIONS).kind, "attention")

    def test_unresolved_thread_needs_attention(self):
        self.assertEqual(evaluate_ready(snapshot(unresolved_threads=1), OPTIONS).kind, "attention")

    def test_new_comment_needs_attention_unless_author_is_ignored(self):
        person = snapshot(new_comments=[{"login": "person", "kind": "comment"}])
        bot = snapshot(new_comments=[{"login": "ci-bot", "kind": "comment"}])
        self.assertEqual(evaluate_ready(person, OPTIONS).kind, "attention")
        self.assertEqual(evaluate_ready(bot, OPTIONS).kind, "ready")

    def test_stacked_pull_request_needs_attention(self):
        verdict = evaluate_ready(snapshot(base="feature-base"), OPTIONS)
        self.assertEqual(verdict.kind, "attention")

    def test_needs_exactly_one_listed_label(self):
        both = snapshot(labels=["safe-to-revert", "unsafe-to-revert"])
        none = snapshot(labels=[])
        self.assertEqual(evaluate_ready(both, OPTIONS).kind, "attention")
        self.assertEqual(evaluate_ready(none, OPTIONS).kind, "attention")

    def test_moved_head_and_draft_need_attention(self):
        self.assertEqual(evaluate_ready(snapshot(head=OLD), OPTIONS).kind, "attention")
        self.assertEqual(evaluate_ready(snapshot(is_draft=True), OPTIONS).kind, "attention")

    def test_merge_conflict_needs_attention(self):
        self.assertEqual(evaluate_ready(snapshot(merge_state="DIRTY"), OPTIONS).kind, "attention")

    def test_edited_summary_comment_blocks_the_queue_when_ready(self):
        edited = snapshot(edited_comments=[{"login": "summary-bot"}])
        verdict = evaluate_ready(edited, OPTIONS)
        self.assertEqual(verdict.kind, "attention")
        self.assertIn("summary-bot", verdict.reasons[0])

    def test_edited_comment_does_not_stop_a_run_that_still_waits(self):
        waiting = snapshot(edited_comments=[{"login": "summary-bot"}], checks=[])
        self.assertEqual(evaluate_ready(waiting, OPTIONS).kind, "wait")

    def test_edit_by_ignored_author_does_not_block(self):
        self.assertEqual(evaluate_ready(snapshot(edited_comments=[{"login": "ci-bot"}]), OPTIONS).kind, "ready")


class PayloadTests(unittest.TestCase):
    def test_reads_latest_payload_state_and_not_condition_text(self):
        old = payload_comment("checking", "2030-01-01T12:00:00Z", updated_at="2030-01-01T12:01:00Z")
        # Condition descriptions can name a check such as "alert-when-failed"; only the state field counts.
        new = payload_comment("checking", "2030-01-01T12:00:00Z", extra=', "note": "alert-when-failed"')
        self.assertEqual(parse_mergify_payload([old, new])["state"], "checking")

    def test_ignores_other_authors_and_bodies_without_payload(self):
        comments = [
            {"login": "person", "body": payload_comment("dequeued", None)["body"], "updated_at": "2030-01-01T12:09:00Z"},
            {"login": "mergify[bot]", "body": "plain text", "updated_at": "2030-01-01T12:09:00Z"},
        ]
        self.assertIsNone(parse_mergify_payload(comments))


class FakeClock:
    def __init__(self):
        self.current = START

    def now(self) -> datetime:
        return self.current

    def sleep(self, seconds: float) -> None:
        self.current += timedelta(seconds=seconds)


def run_watcher(snapshots: list[Snapshot], *, dry_run: bool = False, timeout_minutes: int = 60):
    clock = FakeClock()
    reads = iter(snapshots)
    posts: list[datetime] = []
    last = {"value": snapshots[-1]}

    def fetch(pr, since, own_ids):
        try:
            last["value"] = next(reads)
        except StopIteration:
            pass
        return last["value"]

    def post(pr):
        posts.append(clock.now())
        return 1, clock.now().isoformat().replace("+00:00", "Z")

    watcher = Watcher(
        PullRequest("owner", "repo", 1),
        OPTIONS,
        interval=60,
        timeout=timedelta(minutes=timeout_minutes),
        ack_timeout=timedelta(minutes=5),
        dry_run=dry_run,
        fetch=fetch,
        post=post,
        now=clock.now,
        sleep=clock.sleep,
        log=lambda line: None,
    )
    return watcher.run(), posts


def queued(at: str = "2030-01-01T12:01:00Z") -> dict:
    return {"state": "checking", "queued_at": at, "step": "checks_running"}


class WatcherTests(unittest.TestCase):
    def test_queues_after_two_ready_reads_and_returns_on_merge(self):
        merged = snapshot(state="MERGED", merge_commit="c" * 40, merged_at="2030-01-01T12:30:00Z")
        result, posts = run_watcher([snapshot(), snapshot(), snapshot(mergify=queued()), merged])
        self.assertEqual(posts, [START + timedelta(minutes=1)])
        self.assertEqual(result.code, EXIT_MERGED)
        self.assertEqual(result.extra["merge_commit"], "c" * 40)

    def test_one_ready_read_does_not_queue(self):
        pending = snapshot(checks=[{"name": "aggregate", "state": "PENDING"}])
        result, posts = run_watcher([snapshot(), pending], timeout_minutes=5)
        self.assertEqual(posts, [])
        self.assertEqual(result.code, EXIT_TIMEOUT)

    def test_unacknowledged_queue_comment_needs_attention(self):
        result, posts = run_watcher([snapshot()])
        self.assertEqual(len(posts), 1)
        self.assertEqual(result.code, EXIT_ATTENTION)
        self.assertIn("did not acknowledge", result.reasons[0])

    def test_stale_queue_payload_does_not_count_as_acknowledgement(self):
        stale = snapshot(mergify=queued(at="2030-01-01T10:00:00Z"))
        result, posts = run_watcher([snapshot(), snapshot(), stale])
        self.assertEqual(len(posts), 1)
        self.assertEqual(result.code, EXIT_ATTENTION)
        self.assertIn("did not acknowledge", result.reasons[0])

    def test_already_queued_pull_request_is_followed_without_posting(self):
        merged = snapshot(state="MERGED", merge_commit="c" * 40, merged_at="2030-01-01T12:30:00Z")
        result, posts = run_watcher([snapshot(mergify=queued()), merged])
        self.assertEqual(posts, [])
        self.assertEqual(result.code, EXIT_MERGED)

    def test_leaving_the_queue_needs_attention_after_two_reads(self):
        dequeued = snapshot(mergify={"state": "dequeued", "queued_at": "2030-01-01T12:01:00Z"})
        result, _ = run_watcher([snapshot(mergify=queued()), dequeued, dequeued])
        self.assertEqual(result.code, EXIT_ATTENTION)
        self.assertIn("dequeued", result.reasons[0])

    def test_merged_queue_state_waits_for_github(self):
        mergify_merged = snapshot(mergify={"state": "merged", "queued_at": "2030-01-01T12:01:00Z"})
        merged = snapshot(state="MERGED", merge_commit="c" * 40, merged_at="2030-01-01T12:30:00Z")
        result, _ = run_watcher([snapshot(mergify=queued()), mergify_merged, mergify_merged, mergify_merged, merged])
        self.assertEqual(result.code, EXIT_MERGED)

    def test_dry_run_on_a_queued_pull_request_returns(self):
        result, posts = run_watcher([snapshot(mergify=queued())], dry_run=True)
        self.assertEqual(posts, [])
        self.assertEqual(result.reasons, ["already in the Mergify queue"])

    def test_dry_run_posts_nothing(self):
        result, posts = run_watcher([snapshot()], dry_run=True)
        self.assertEqual(posts, [])
        self.assertEqual(result.reasons[0], "would queue")

    def test_finding_before_ready_returns_attention_without_posting(self):
        result, posts = run_watcher([snapshot(unresolved_threads=2)])
        self.assertEqual(posts, [])
        self.assertEqual(result.code, EXIT_ATTENTION)


if __name__ == "__main__":
    unittest.main()
