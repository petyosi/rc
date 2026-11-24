#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' 'Usage: run-review.sh [--target DESCRIPTION] [--base REF | --pr NUMBER] [--model MODEL] [--output FILE]'
}

target='current branch against its base, including staged, unstaged, and untracked changes'
base=''
pr=''
model='gemini-4-neon-high'
output=''

while (($#)); do
  case "$1" in
    --target|--base|--pr|--model|--output)
      [[ $# -ge 2 ]] || { usage >&2; exit 2; }
      declare "${1#--}=$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

command -v agy >/dev/null 2>&1 || {
  printf '%s\n' 'Antigravity CLI (agy) is not installed or is not on PATH.' >&2
  exit 127
}

repo=$(git rev-parse --show-toplevel 2>/dev/null) || {
  printf '%s\n' 'Run this command from inside the repository to review.' >&2
  exit 2
}

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
contract=$(cd "$script_dir/../../code-review" && pwd)/SKILL.md
[[ -r "$contract" ]] || {
  printf 'Review contract not found: %s\n' "$contract" >&2
  exit 2
}

# BSD mktemp only substitutes trailing X's, so use a directory to keep the .md suffix.
work=$(mktemp -d "${TMPDIR:-/tmp}/agy-cold-review.XXXXXX")
cp "$contract" "$work/contract.md"
diff_file=$work/target.diff

# The diff is prepared here because agy cannot ask for command approval in print mode, and the
# sandbox it runs in has no network for `gh`.
(
  cd "$repo"
  if [[ -n "$pr" ]]; then
    gh pr view "$pr" --json url,title,body,baseRefName,headRefName \
      --template '{{.url}}{{"\n"}}{{.headRefName}} -> {{.baseRefName}}{{"\n\n"}}{{.title}}{{"\n\n"}}{{.body}}{{"\n"}}' \
      >"$work/pr.md"
    gh pr diff "$pr" >"$diff_file"
  else
    if [[ -z "$base" ]]; then
      base=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null || true)
      for candidate in origin/main origin/master main master; do
        [[ -n "$base" ]] && break
        git rev-parse --verify --quiet "$candidate" >/dev/null && base=$candidate
      done
    fi
    [[ -n "$base" ]] || { printf '%s\n' 'Cannot find a base branch; pass --base.' >&2; exit 2; }
    merge_base=$(git merge-base "$base" HEAD)
    {
      printf '# Base: %s (merge base %s)\n' "$base" "$merge_base"
      git log --format='# %h %s' "$merge_base..HEAD"
      git diff "$merge_base"
      while IFS= read -r -d '' file; do
        git diff --no-index -- /dev/null "$file" || true
      done < <(git ls-files --others --exclude-standard -z)
    } >"$diff_file"
  fi
)

[[ -s "$diff_file" ]] || { printf '%s\n' 'The review target has no changes.' >&2; exit 2; }

pr_line=''
[[ -n "$pr" ]] && pr_line="Pull request description: $work/pr.md"

prompt=$(printf '%s\n' \
  'Perform a cold, independent code review. Do not edit files or change external state.' \
  "Repository: $repo" \
  "Review target: $target" \
  "Complete diff of the target: $diff_file" \
  "$pr_line" \
  "Review contract: $work/contract.md" \
  '' \
  'Read the complete review contract and follow it, with these differences:' \
  '- The diff file above is the target. You do not need to compute it.' \
  '- Do not delegate to subagents and do not browse the web.' \
  '- Prefer your file viewing and search tools. Shell commands are limited to the read-only' \
  '  commands git diff, git log, git show, git blame, git status, git ls-files, rg, grep, ls,' \
  '  cat, head, tail and wc, as plain commands without redirects, pipes, or command substitution.' \
  '  Any other command is refused and ends the review without a report.' \
  'Return only the final review report, in the format the contract specifies, as your last message.')

# A linked worktree keeps its history in the main checkout's .git, outside the sandbox workspace.
git_dir=$(cd "$repo" && cd "$(git rev-parse --git-common-dir)" && pwd)

# Deny rules apply in every mode. Allow rules match by literal word prefix.
settings=$(python3 -c '
import json, sys
allow = ["git diff", "git log", "git show", "git blame", "git status", "git ls-files",
         "rg", "grep", "ls", "cat", "head", "tail", "wc"]
print(json.dumps({"permissions": {
    "allow": [f"command({c})" for c in allow] + [f"read_file({path})" for path in sys.argv[1:]],
    "deny": ["write_file(*)", "read_url(*)", "execute_url(*)", "mcp(*)"],
}}))' "$repo" "$work" "$git_dir")

log=$work/agy.jsonl
run=(agy --print "$prompt" --mode plan --sandbox --model "$model" --output-format stream-json
  --settings "$settings" --add-dir "$work" --add-dir "$git_dir")
watchdog=$HOME/.claude/scripts/agent-watchdog.sh
status=0
(
  cd "$repo"
  if [[ -x "$watchdog" ]]; then
    "$watchdog" --log "$log" -- "${run[@]}"
  else
    "${run[@]}" </dev/null >"$log" 2>&1
  fi
) || status=$?

report=$work/report.md
python3 - "$log" "$report" <<'PY' || { printf 'agy run failed (exit %s); log: %s\n' "$status" "$log" >&2; exit 1; }
import json, sys
log, report = sys.argv[1:]
result = None
for line in open(log, errors="replace"):
    if line.startswith("{"):
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("event") == "result":
            result = event["result"]
if result is None:
    sys.exit("agy produced no result event")
usage = result.get("usage", {})
print(f"agy status={result.get('status')} total_tokens={usage.get('total_tokens')}", file=sys.stderr)
if result.get("denied_actions"):
    print(f"agy denied actions: {json.dumps(result['denied_actions'])}", file=sys.stderr)
response = (result.get("response") or "").strip()
if result.get("status") != "SUCCESS" or not response:
    sys.exit(f"agy returned no review: {result.get('error') or 'empty response'}")
open(report, "w").write(response + "\n")
PY

if [[ -n "$output" ]]; then
  output=$(cd "$(dirname "$output")" && pwd)/$(basename "$output")
  mv "$report" "$output"
  report=$output
fi

printf '\nREPORT_PATH=%s\nAGY_LOG=%s\n' "$report" "$log"
