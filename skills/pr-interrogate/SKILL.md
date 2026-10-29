---
name: pr-interrogate
description: Interrogate branch or pull request changes before opening a PR, so that every addition traces to the stated intent and has a cited justification. Use when the user asks to interrogate changes, check a branch for scope creep or over-engineering, make an agent justify what it built, or run a pre-PR scope check. Complements code-review, which hunts defects; this skill asks whether each change should exist. Read-only.
---

# PR Interrogation

Line-by-line review of a large agent-written diff misses the main risk: code that is correct but was never needed. Reviewers that see only the diff treat extra tables, jobs, flags, and abstractions as deliberate. Treat the PR as testimony instead. Inventory what it adds, question each addition against the stated intent, and keep only what cited evidence supports.

This skill does not hunt defects. Use `code-review` for correctness.

Keep the run read-only. Do not edit files, alter git state, post comments, or update pull requests.

## 1. Resolve the target and intent

Default target: the current branch against its base, including staged, unstaged, and untracked changes. For a pull request, use read-only `gh pr view` and `gh pr diff`.

Collect intent from these sources, strongest first:

1. A PRP or plan file that the user names, or one in the repository that matches the branch. Its scope and `CX-N` scenarios are the contract.
2. The pull request description and linked issues.
3. The user's request in this session, when this session implemented the change.
4. Commit messages. They describe what was built, not what was asked, so confirm them with the user before relying on them alone.

If no source exists, ask the user for one or two sentences of intent. Do not continue without intent; scope cannot be judged without it.

Write an intent brief: the requested outcome, explicit non-goals, and known constraints. Do not invent non-goals. If none are stated, record that.

## 2. Inventory with a fresh subagent

Start one fresh subagent with no conversation history. Give it only the repository path, the target, and the instructions below. Do not give it the intent brief or any suspicions, so that its descriptions stay neutral.

> List what this change adds, alters, and removes. Do not judge the code or explain why it exists. Report each item with file:line and a concrete one-line description of its trigger, inputs, and effect. Cover:
> - schema, migrations, and other persisted state, including caches
> - background jobs, schedules, retries, and queues
> - public surface: endpoints, exports, CLI flags, events
> - configuration: environment variables, flags, and options with their defaults
> - dependencies
> - new modules, abstractions, and interfaces, with the number of implementations and callers
> - validation, error handling, and fallback paths
> - tests, and the items they exercise
> - deletions and behavior changes
>
> If you cannot state an item's effect concretely from the code, write `PURPOSE NOT EVIDENT` and quote the wording that the code or comments use for it.

Group trivial items, such as renames, under one line. If a fresh subagent is unavailable, write the inventory yourself and record the independence limit.

## 3. Ask the user for external facts

Identify facts that only the user can supply: deployment shape, scale, roadmap, team conventions, and planned integrations. Ask for them in one batch before interrogation; use AskUserQuestion when it is available. Skip this step when no such questions exist. Add the answers to the intent brief.

## 4. Build the questions

Map each inventory item to the intent brief:

- `TRACED`: an intent line requires it. Cite the line.
- `SUPPORTING`: a traced item requires it. Cite the dependency.
- `UNTRACED`: neither applies.

Question every `UNTRACED` item, every `PURPOSE NOT EVIDENT` item, and every `SUPPORTING` item that adds a new kind of thing: persisted state, a job, a dependency, configuration, public surface, or an abstraction with one implementation. Also question each behavior that the intent promises: where it is enforced, and which test fails if it breaks.

Phrase questions neutrally. A leading question such as "Isn't this unnecessary?" invites capitulation, which is as unreliable as an invented reason to keep the item. Use forms such as:

- Which requirement does <item> serve? Quote it.
- Which existing <table, service, utility> could do this, and why does it not? Cite it.
- Who will change <setting> from its default, and when?
- What does <dependency> do that the codebase or standard library cannot?
- Which caller needs <abstraction>, and where is its second implementation?
- What stops working in the stated outcome if <item> is removed?
- Where is <behavior> enforced, and which test fails if it breaks?

## 5. Take testimony

Select the witness:

- If this session implemented the change, answer from your own knowledge of why you built each item.
- Otherwise, start a fresh subagent to reconstruct the reasons from commits, the pull request description, linked issues, and code comments. Mark this testimony `RECONSTRUCTED`.

Each answer must cite evidence that the judge can open: a quote from the intent brief, a file:line in code that existed before this change, a test name, an external document, observed environment state with the command that shows it, or a fact the user supplied. "Defensive", "best practice", "future-proof", or "for flexibility" without a named consumer is not evidence. Do not change code during testimony.

## 6. Judge with a fresh subagent

Start one fresh subagent with no conversation history. Give it the repository path, the target, the intent brief, the full inventory with the step 4 mapping, and each question with its answer and citations. Do not give it the witness's other reasoning.

Instruct it to challenge every `TRACED` or `SUPPORTING` item whose cited intent line or dependency does not require it, and to judge that item as `UNJUSTIFIED`. The mapping is written by the orchestrator, which may be the implementer, so it must not pass unchecked.

Instruct it to open every citation and assign one verdict per item:

- `JUSTIFIED`: the citation exists and supports the answer.
- `UNJUSTIFIED`: no citation, a citation that does not say what is claimed, a circular citation that points only to code added by this change, a generic principle, or a capitulation that does not state what removal would break.
- `OUT_OF_SCOPE`: the reason is real, but it serves a non-goal or an outcome that the intent does not include.
- `UNPROVEN`: a promised behavior with no enforcement at the cited location or no test that would fail.

Instruct it to disagree whenever evidence is missing. Agreement without evidence is the failure that this step exists to prevent. Instruct it also to verify, not accept, factual side claims in the testimony.

## 7. Report

Check each non-`JUSTIFIED` verdict against the cited code before you present it. Then report:

---

## PR Interrogation

**Target:** {target}
**Intent:** {sources}; non-goals {stated | not stated}
**Witness:** {implementer | reconstructed}
**External facts:** {facts the user supplied, or none}

### Needs a decision

List new persisted state, public surface, dependencies, and jobs first.

**{N}. {item}** ({verdict})

- **Location:** {file:line}
- **Question:** {question}
- **Testimony:** {one-line answer}
- **Why it fails:** {judge's reason}
- **If removed:** {what the witness says would break, or nothing}

### Justified

One line per item: {item} → {citation}.

### Traced without questions

One line per `TRACED` or `SUPPORTING` item that was not questioned: {item} → {intent line or dependency}.

### Incidental defects

Defects that the witness or judge confirmed in passing, with file:line and the reproduction. Omit this section when there are none. Do not search for defects; that is the work of `code-review`.

### Limits

State missing non-goals, reconstructed testimony, an inventory written without a fresh subagent, or parts of the change left unexamined.

---

Do not remove or change anything. Ask the user which items to cut, which to justify further, and which to accept.
