---
name: mergify-land-watch
description: Wait in the background until a pull request is merge-ready, post `@mergifyio queue`, and follow the Mergify queue until the pull request merges. Use in a land-pr or "land this PR" workflow, in a repository that queues with Mergify, after each settled push, so the user does not have to watch the pull request. Do not use it to judge review findings. The watcher stops on a finding and hands it back to the agent.
---

# Mergify land watch

`scripts/land_watch.py` replaces the wait in a land workflow. It reads the pull request once a minute. It posts
`@mergifyio queue` only when the pull request is merge-ready on the head that the agent reviewed. Then it follows the
Mergify queue until GitHub reports the merge. It stops on every state it does not recognize, so the agent stays
responsible for each review finding.

## When to start it

Start the watcher after each settled push, when no **Ask** item is open and every finding that you know of has a
fix or a reply. The `--head` value is the SHA that you reviewed. It is the permission to queue that head and no
other.

Keep the app PR monitor (Auto-fix) on when it is available. The monitor wakes the agent on CI failures, conflicts
and comments. The watcher covers what the monitor does not report: green checks, an approval, and the merge.

## Command

Run it as a background command, with the absolute path of the installed script, so one permission rule covers it:

```bash
~/.claude/skills/mergify-land-watch/scripts/land_watch.py "$PR_URL" \
  --head "$REVIEWED_SHA" \
  --required-check "$AGGREGATE_CHECK" \
  --one-of-label "$LABEL_A,$LABEL_B" \
  --ignore-commenter "$BOT_LOGIN_REGEX"
```

Take the repository values from the project's memory or `AGENTS.md`:

- `--required-check`: the CI aggregate check that the queue requires. Repeat the flag for more checks. The flag is
  required, so an empty check list never reads as green.
- `--one-of-label`: labels of which exactly one must be set, such as revertibility labels.
- `--ignore-check`: a regex of check names that end neutral by design. The default is `^Mergify `.
- `--ignore-commenter`: a regex of logins whose new top-level comments carry no finding, such as a queue bot or
  a deploy preview bot. A reviewer bot that can post a finding as a top-level comment stays out of this regex.

Run it once with `--dry-run` on a new repository. It reads the pull request one time, prints the verdict, and posts
nothing. A dry run that finds a reason to stop returns `attention` with exit code 3, as a real run does.

## What it checks before it queues

The pull request is ready when all of these hold on two reads in a row:

- It is open, it is not a draft, its head is `--head`, and its base is the default branch.
- Exactly one `--one-of-label` label is set, and the base branch has no conflict.
- Every `--required-check` succeeded. No other check is pending. Every other check is `SUCCESS` or `SKIPPED`.
- An approval from a reviewer with push access is on `--head`. No review requests changes, and GitHub does not
  report `REVIEW_REQUIRED`.
- No review thread is unresolved. No new top-level comment or review comment arrived after the start, other than
  from `--ignore-commenter`.
- No earlier comment was edited after the start, other than by `--ignore-commenter` or a Mergify status comment. A
  summary bot fills in pre-merge findings by editing one comment. The watcher checks edits only at the ready
  moment, so a bot that edits its summary while checks run does not stop the run early.

After the post, the watcher requires a Mergify status whose `queued_at` is later than the comment. It reads only
the structured Mergify status and the GitHub pull request state, never the comment text. Mergify writes the status
values `checking`, `merged` and `dequeued`, with a new status comment for each queue attempt. A `merged` status
waits for GitHub to report the merge. Any other value than `checking` or `merged` on two reads returns `attention`.

## Exit codes

The last line of the output is `RESULT {json}` with `result`, `reasons`, and on a merge `merge_commit` and
`merged_at`.

| Code | Result | Action |
| --- | --- | --- |
| 0 | `merged` | Check that `merge_commit` is on the base branch, then report the merge time and commit. |
| 0 | `dry-run` | Read the verdict. |
| 3 | `attention` | Read each reason on the pull request. Fix, reply, or ask the user, then start a new run. |
| 4 | `timeout` | Read the pull request state, then start a new run or report the wait. |
| 1 | `error` | Five reads failed in a row. Check `gh auth status` and the network. |
| 2 | usage | Fix the arguments. |

A check that ends `NEUTRAL` outside `--ignore-check` returns `attention`, because an AI reviewer reports a finding
as a neutral conclusion.

## Limits

- The watcher cannot judge the text of an edited summary comment. It stops and hands the comment to the agent. A
  bot that keeps editing its summary can stop each run once, so read it and start a new run.
- It does not queue a stack. A base other than the default branch returns `attention`, and the stack procedure of
  the land workflow applies.
- It never retries or requeues. A dequeue returns `attention` with the Mergify state.

## Tests

```bash
cd ~/.claude/skills/mergify-land-watch/scripts && python3 -m unittest test_land_watch
```
