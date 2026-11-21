#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' 'Usage: run-review.sh [--target DESCRIPTION] [--output FILE]'
}

target='current worktree, including committed, staged, unstaged, and untracked changes'
output=''

while (($#)); do
  case "$1" in
    --target)
      [[ $# -ge 2 ]] || { usage >&2; exit 2; }
      target=$2
      shift 2
      ;;
    --output)
      [[ $# -ge 2 ]] || { usage >&2; exit 2; }
      output=$2
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

command -v claude >/dev/null 2>&1 || {
  printf '%s\n' 'Claude CLI is not installed or is not on PATH.' >&2
  exit 127
}

repo=$(git rev-parse --show-toplevel 2>/dev/null) || {
  printf '%s\n' 'Run this command from inside the repository to review.' >&2
  exit 2
}

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
skill_dir=$(cd "$script_dir/.." && pwd)
contract="$skill_dir/../code-review/SKILL.md"
[[ -r "$contract" ]] || {
  printf 'Review contract not found: %s\n' "$contract" >&2
  exit 2
}

requested_output=$output
report_dir=$(mktemp -d "${TMPDIR:-/tmp}/claude-cold-review.XXXXXX")
report_file=$report_dir/report.md
if [[ -n "$requested_output" ]]; then
  output=$(cd "$(dirname "$requested_output")" && pwd)/$(basename "$requested_output")
else
  output=$report_file
fi

prompt_file=$report_dir/prompt.txt
trap 'rm -f "$prompt_file"' EXIT

printf '%s\n' \
  'Perform a cold, independent code review. Do not edit files or change external state.' \
  "Repository: $repo" \
  "Review target: $target" \
  "Review contract: $contract" \
  '' \
  'Read the complete review contract and follow it.' \
  'Return only the final review report, in the format the contract specifies.' \
  >"$prompt_file"

(
  cd "$repo"
  env -u ANTHROPIC_API_KEY claude --print \
    --model fable \
    --effort medium \
    --safe-mode \
    --no-session-persistence \
    --permission-mode dontAsk \
    --add-dir "$skill_dir" \
    --add-dir "$(dirname "$contract")" \
    --allowedTools 'Bash(git *),Bash(gh pr view *),Bash(gh pr diff *),Read,Glob,Grep,Task' \
    --disallowedTools 'Edit,Write,NotebookEdit,WebFetch,WebSearch' \
    <"$prompt_file" \
    | tee "$report_file"
)

if [[ -n "$requested_output" ]]; then
  mv "$report_file" "$output"
fi

printf '\nREPORT_PATH=%s\n' "$output"
