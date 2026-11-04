---
name: start-today
description: Start work on today's scheduled tasks. Reads the open rows that are due today or overdue in the user's Notion "Scheduled tasks" database, checks whether each blocker has cleared, then, with the user's approval, starts a session, does a quick check here, moves the date, or closes the row. Use when the user asks what is due today, to start or work on today's items or tasks, to go through scheduled follow-ups, or to clear overdue tasks.
---

# Start Today's Tasks

The user schedules tasks as rows in a Notion database (see the `schedule-task` skill). This skill turns the rows that are due into work and records each result on its row, so the row's state is always current.

- Database: https://app.notion.com/p/591a5c9e21f441d783710371974a9ffb
- Data source: `collection://9470f253-cd2e-4cee-9c96-8cdaa6d181a0`
- Open statuses: `Not started`, `Waiting`, `In progress`. Closed statuses: `Done`, `Dropped`, `Archived`.

Steps 1 to 3 change nothing. Do not update rows, start sessions, or run write commands before the user approves in step 4.

## 1. Read the due rows

Query the data source for open rows with a `Due` date on or before the end of today in the user's local time zone. Overdue rows count. Notion stores `Due` in UTC, so compare local dates, not the UTC text. Sort by `Due`.

For each row, fetch the page: the body has the blocker check and the brief. Read its comments too, because a comment can record a session that already started or a check that already ran.

If no row is due, say so, name the next due row and its date, and stop.

## 2. Check each blocker

For each row with `Waits on` set, run the blocker check from its body when the check is read-only and short, such as one `gh` command, a `git merge-base --is-ancestor` test against a deploy SHA, or one query. Do not run the full brief here. Give each row one result:

- **Cleared**: the check shows that the deploy, merge, release, reply, or time window happened.
- **Not cleared**: the check shows that it did not happen yet. Estimate when it will, from the evidence.
- **Unknown**: the check needs access you do not have, or the body has no check.

Also look for rows that are stale: the linked PR is closed without a merge, a later PR replaced it, or another row covers the same check.

## 3. Propose an action for each row

Give each row one recommended action:

- **Start session**: the blocker cleared and the work needs more than a few tool calls, or it ends in a branch or PR.
- **Do here**: a read-only check or a short task that a few tool calls finish.
- **Move**: the blocker has not cleared. Propose a new date from the estimate, or 7 days from today when there is none.
- **Done** or **Drop**: the work already happened, or the row is stale. Give the evidence.
- **Yours**: a `Personal` row, or a `Decision` that only the user can make. List it with no action from you.

Show a short report:

---

## Due today: {date}

| Task | Due | Blocker | Action |
|---|---|---|---|
| [{title}]({row url}) | {local date, time; "overdue" if before today} | {cleared / not cleared / unknown: evidence} | {action, new date if Move} |

---

Then ask in one batch, with AskUserQuestion when it is available. Use multi-select questions so the user can approve each action. Put your recommendation first. When a row you propose to move has open `Blocking` rows due before its new date, ask whether to move those rows too.

## 4. Act on approved actions

Record every result on its row: set `Status`, and add a comment with the date and the outcome. A comment is the row's history, so never only change a property.

- **Start session.** Start one session for each approved row with the desktop app's `start_session`: `initiation: "user_asked"`, `context: "fresh"`. The prompt is the brief from the row body, plus this closing instruction: "When you finish, update the Notion row {row url}: set Status to Done, or to Waiting with a new Due date if the work must wait again, and add a comment with the result and any PR link." Then set the row to `In progress` and add a comment that names the session. Start sessions only for rows that are independent: a row that is `Blocked by` an open row waits for it. If `start_session` is not available, print each brief as a paste-ready prompt and leave the row status unchanged.
- **Do here.** Do the check or the task. Then set `Done`, or `Waiting` with a new `Due`, and add a comment with the result and evidence links.
- **Move.** Set the new `Due` with the UTC offset that applies on that date, keep or set `Waiting`, and add a comment: "Moved from {old date} to {new date}: {reason}." Move the approved `Blocking` rows the same way.
- **Done** or **Drop.** Set the status and add a comment with the evidence.

## 5. Summarize

List each row with what happened, as a link: sessions started (with session links), checks done and their results, rows moved and their new dates, and rows closed. List each approved action that failed, with the reason. Keep it short.
