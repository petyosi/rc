---
name: schedule-task
description: Schedule a task for a later date as a row in the user's Notion "Scheduled tasks" database, which Notion Calendar shows on the user's calendar. Use when the user asks to schedule something, remind them, follow up later, check something after a deploy, merge, release or reply, revisit a decision on a date, or "put it on my calendar" as a task. Also use when another skill (such as close-out) routes a follow-up that waits on something. Do not use for a meeting with other people or for a repeating routine; those stay in Google Calendar.
---

# Schedule a Task

The user keeps dated tasks in one Notion database, not in Google Calendar. A calendar event has no state: each delay used to create a new event, and nobody recorded the outcome. A database row has a status, a due date, a blocker, and a brief, and the row moves when the date moves. Notion Calendar shows each row on its `Due` date, so the row is also the calendar entry. Do not create a Google Calendar event as well.

## The database

- Name: "Scheduled tasks", a private database in the Pydantic Notion workspace.
- URL: https://app.notion.com/p/591a5c9e21f441d783710371974a9ffb
- Data source: `collection://9470f253-cd2e-4cee-9c96-8cdaa6d181a0`

| Property | Type | Value |
|---|---|---|
| `Task name` | title | A short imperative title. No `Follow-up:` prefix. |
| `Status` | status | `Not started`, `Waiting`, `In progress`, `Done`, `Dropped`, `Archived`. |
| `Kind` | select | `Check`, `Decision`, `To-do`, `Reading`, `Personal`. |
| `Due` | date | Date and time. Set `date:Due:start` and `date:Due:is_datetime` = 1. |
| `Waits on` | text | The blocker in one line: the deploy, merge, release, reply, or time window. |
| `Link` | url | The main PR, issue, alert, or document. |
| `Blocked by` / `Blocking` | relation | Other rows in the same database. |
| `Assignee` | person | The connected Notion user. |

If a property name or option in this table does not match the fetched schema, trust the schema and tell the user that this skill is out of date.

## What does not belong here

- A meeting or call with other people. Create a Google Calendar event for it.
- A repeating routine, such as weekly dependabot triage. It stays a repeating Google Calendar event.
- Work that can start now. Offer to do it, or to start a session for it.
- A GitHub issue's own status. If the item has an issue, the issue keeps its status on the GitHub board. The row holds only when to look and what to check, and links the issue.

## 1. Collect the task

Take each field from the user's words and the conversation. Ask only for what you cannot infer, in one question.

- **What.** The title, and the `Kind`:
  - `Check` waits on something outside the session: a deploy, merge, soak period, release, reply, or measurement window.
  - `Decision` is a choice to make on a date.
  - `To-do` is work that can start only later.
  - `Reading` is something to read or look into.
  - `Personal` is a non-work errand. Keep the user's own words and language in the title.
- **When.** Compute absolute dates from today's date. For "Friday", "next week" or "in 3 days", give the computed date in your reply. If the user gives no time, use 10:00. If the user gives no date, propose one: the time the blocker is expected to clear, or 7 days from today when nobody knows. Ask before you write the row.
- **Time zone.** Use the user's local time zone. Write `date:Due:start` as ISO 8601 with the UTC offset that applies on that date, for example `2026-11-10T10:00:00+02:00`. The offset changes with daylight saving time, so compute it for the due date, not for today. Notion stores the value in UTC, so a read-back of `08:00:00Z` for 10:00 at +02:00 is correct.
- **Waits on.** The blocker, and how to see that it has cleared. Leave it empty when the task waits only on the date.
- **Link.** The main URL, if there is one.

## 2. Write the brief

The page body is what the user, or a new session, reads on the due date. That reader has not seen this conversation.

- For `Check`, `Decision` and `To-do` items that come from a working session, the body holds:
  - **How to check that the blocker has cleared**, with the exact command, query, or place to look.
  - **A paste-ready brief**: the task and what done looks like; the repository path, base branch, and PR and issue URLs; the decisions and constraints from this session; the files or area to start from.
- For a simple reminder or a `Personal` item, the body can be one line, or empty.

Write absolute dates and full URLs. Do not write "today", "the PR above", or "as discussed".

## 3. Find an existing row first

Query the data source for open rows: `Status` in `Not started`, `Waiting`, `In progress`. Look for a row with the same `Link`, or with a title about the same check.

- **Same check.** Update that row. Move `Due`, rewrite `Waits on`, and replace the brief in the body. Add a comment that says what changed and why, for example "Moved to 2026-11-12: the deploy had not happened on 2026-11-10". Do not create a second row.
- **A new check that can start only after another open row is done.** Create a new row and set its `Blocked by` to that row.
- **Two open rows about the same check.** Tell the user and offer to merge them. Do not merge them without approval.

## 4. Create or update the row

Create the page in the data source. Set:

- `Task name`, `Kind`, `Due`, `Waits on`, `Link` from step 1.
- `Status`: `Waiting` when `Waits on` is set. Otherwise `Not started`.
- `Assignee`: the connected user, from the Notion connector's "get self" tool.
- The page body from step 2.

The user's request to schedule the task is the approval. Do not ask again before you write, except to fill a missing date.

## 5. Report

Give one line for each row: the title as a link to the row, the due date and time in local time, and the blocker. Say whether you created the row or updated an existing one.

If the Notion connector is not available, do not use Google Calendar or a scheduled agent instead. Tell the user, and print the title, date, blocker and brief so they can add the row by hand.
