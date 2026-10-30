---
name: close-out
description: Close out a coding session after its work is done, typically after the pull request is merged. Inventories what is still pending (uncommitted work, unpushed commits, open review threads, failing checks, running side sessions, deferred items), then routes each follow-up to a new session when it is ready or to a Google Calendar event when it waits on something. Use when the user says to close out, wrap up, or finish the session, asks what is left or pending, or says the PR is merged and wants to move on.
---

# Session Close-Out

A session ends with loose threads: work that was deferred, review comments marked for later, checks that need a re-run after a release. If nothing records them, they are lost when the session is archived. This skill finds each thread, decides where it goes, and gets the user's approval before anything happens.

Steps 1 to 3 are read-only. Do not change files, git state, pull requests, sessions, or calendars before the user approves in step 4.

## 1. Inventory the session

Collect state from each source that applies. Skip a source that does not exist; record skipped sources for the report.

**Git**, in the session's working directory:

- `git status --porcelain` and `git stash list`: uncommitted, untracked, and stashed work.
- Current branch, its upstream, and `git log @{upstream}..HEAD`: unpushed commits.
- Whether the branch is merged into the base branch, and whether its remote branch still exists.
- `git worktree list`: a worktree that this session created and no longer needs.

**Pull request**, when `gh` is available and the branch has one:

- `gh pr view --json number,url,state,mergedAt,reviewDecision,statusCheckRollup,closingIssuesReferences`.
- Unresolved review threads, through `gh api graphql` on `pullRequest.reviewThreads` with `isResolved`. A reviewer's "follow-up", "later", or "separate PR" comment is a follow-up even when its thread is resolved.
- Failing or pending checks, and linked issues that are still open after the merge.

**The diff**: `TODO`, `FIXME`, `XXX`, and `HACK` lines that this branch added. Search the diff against the base branch, not the whole repository.

**The conversation**:

- Items that you or the user called a follow-up, out of scope, a separate PR, later, or a known limitation.
- Task-list steps that are not completed, and steps that were skipped.
- Session proposals made in this session that the user did not start.
- Verification that was planned but not done: a manual check, a deploy check, a release step.

**The environment**, when the tools exist:

- Sessions started from this one (the desktop app's `list_sessions` with `linked: true`): running sessions, and finished sessions whose branches are not merged.
- Background tasks, dev servers, scheduled tasks, and cron jobs that this session started.

## 2. Classify each item

Put each item in exactly one class:

- **Pending**: it must be done before the session closes, because the work is lost or broken otherwise. Examples: uncommitted changes, unpushed commits, a running side session, a failing check on the merged commit.
- **Ready**: a follow-up that can start now. You can write a complete brief from what this session knows, and nothing external blocks it.
- **Not ready**: a follow-up that waits on something outside the session: a release, a deploy, a soak period, another PR, a person's reply, or a date. Name the blocker and estimate when it clears. Use a concrete date computed from today's date; when no estimate exists, propose 7 days from today.
- **Drop**: not worth doing. Give the reason in one line.
- **Cleanup**: local housekeeping after a merge: delete the merged local branch, remove the worktree, stop servers, archive the session.

Merge duplicates. Do not invent follow-ups to fill a class; an empty class is a normal result.

## 3. Report and ask

Show the report:

---

## Close-out

**Session:** {repository} on {branch}; PR {url and state, or none}
**Sources checked:** {list}; skipped: {list with reason}

### Pending
- {item} — {why it blocks closing} — {proposed action}

### Ready → new session
- **{title}** — {one-line scope}

### Not ready → calendar
- **{title}** — waits on {blocker} — proposed {date}

### Drop
- {item} — {reason}

### Cleanup
- {action}

---

Then ask in one batch, with AskUserQuestion when it is available. Use multi-select questions so the user can approve each item: which pending actions to take, which sessions to start, which calendar events to create and on which dates, and which cleanup actions to run. Put your recommendation first. Move an item between classes when the user says so.

If there is nothing in any class, say that the session can close, and offer to archive it.

## 4. Act on approved items

Do the approved actions in this order, because later steps depend on earlier ones.

**Pending.** Commit, push, re-run checks, or wait for a side session, as approved. Follow the repository's commit conventions. Do not force-push or discard work without a separate, explicit approval.

**Ready → new session.** Start one session for each approved item with the desktop app's `start_session`: `initiation: "user_asked"`, `context: "fresh"`, a complete `prompt`, and `background`. The new session has not seen this conversation, so the brief must include:

- the task, and what done looks like;
- the repository path, the base branch, and related PR and issue URLs;
- the decisions and constraints from this session that apply;
- the files or area to start from.

Each session gets its own worktree when it ends in its own branch or PR. If `start_session` is not available, for example in Codex or the CLI, print each brief as a paste-ready prompt and tell the user that no session was started.

**Not ready → calendar.** Create one event for each approved item with the Google Calendar connector's `create_event` tool, on the user's primary calendar:

- `summary`: `Follow-up: {title}`.
- `startTime` and `endTime`: a 30-minute block at 10:00 on the approved date, unless the user gave a time. Give local time with no offset, and leave `timeZone` unset unless the user named one.
- `description`: the blocker, how to check that it has cleared, and the same complete brief as for a new session. The user must be able to start the follow-up by pasting the description into a new session.
- No attendees. An attendee receives an invitation, which sends a message on the user's behalf.

If the Google Calendar connector is not available, do not use another calendar or a scheduled agent instead. Tell the user, and print each event's title, date, and description so they can add it.

**Cleanup.** Run the approved actions. Delete a local branch only after you confirm that it is merged. Remove a worktree only after you confirm that it has no uncommitted work. Archive the session last, and only when the user approved it, because archiving ends this session.

## 5. Summarize

List what was done, with links: commits pushed, sessions started, calendar events created, and cleanup done. List each approved item that failed, with the reason. Keep it short.
