#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' 'Usage: run-review.sh [--target DESCRIPTION] [--output FILE] [--effort LEVEL]'
}

target='current worktree, including committed, staged, unstaged, and untracked changes'
output=''
# Astra in Fast mode is the only permitted reviewer configuration, so no flag can override it.
readonly model='gpt-6-astra'
readonly service_tier='priority'
effort='high'

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
    --effort)
      [[ $# -ge 2 ]] || { usage >&2; exit 2; }
      effort=$2
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

command -v codex >/dev/null 2>&1 || {
  printf '%s\n' 'Codex CLI is not installed or is not on PATH.' >&2
  exit 127
}

repo=$(git rev-parse --show-toplevel 2>/dev/null) || {
  printf '%s\n' 'Run this command from inside the repository to review.' >&2
  exit 2
}

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
skill_dir=$(cd "$script_dir/.." && pwd)
# The sibling code-review skill is the single source of truth for the review contract.
contract=$(cd "$skill_dir/../code-review" && pwd)/SKILL.md
[[ -r "$contract" ]] || {
  printf 'Review contract not found: %s\n' "$contract" >&2
  exit 2
}

requested_output=$output
# BSD mktemp only substitutes trailing X's, so use a directory to keep the .md suffix.
report_dir=$(mktemp -d "${TMPDIR:-/tmp}/codex-cold-review.XXXXXX")
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
  'Return only the final review report, in the format the contract specifies, as your last message.' \
  >"$prompt_file"

# Set the tier explicitly so the review does not inherit whatever the user's config selects.
model_args=(--model "$model" -c "model_reasoning_effort=\"$effort\"" -c "service_tier=\"$service_tier\"")

(
  cd "$repo"
  # notify=[] suppresses the interactive turn-ended hook from the user's config.
  codex exec \
    --sandbox read-only \
    --ephemeral \
    --skip-git-repo-check \
    -c 'notify=[]' \
    "${model_args[@]}" \
    --output-last-message "$report_file" \
    - <"$prompt_file"
)

if [[ -n "$requested_output" ]]; then
  mv "$report_file" "$output"
fi

printf '\nREPORT_PATH=%s\n' "$output"
