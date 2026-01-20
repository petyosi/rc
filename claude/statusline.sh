#!/bin/bash
# Claude Code statusline script
# Shows: Model | Context usage | Tokens

json=$(cat)

# Extract values using jq
model=$(echo "$json" | jq -r '.model.display_name // "Unknown"')
context_pct=$(echo "$json" | jq -r '.context_window.used_percentage // 0')
input_tokens=$(echo "$json" | jq -r '.context_window.total_input_tokens // 0')
output_tokens=$(echo "$json" | jq -r '.context_window.total_output_tokens // 0')

# Format tokens (K notation)
format_tokens() {
    local tokens=$1
    if [ "$tokens" -ge 1000 ] 2>/dev/null; then
        awk "BEGIN {printf \"%.1fK\", $tokens / 1000}"
    else
        echo "$tokens"
    fi
}

input_fmt=$(format_tokens "$input_tokens")
output_fmt=$(format_tokens "$output_tokens")

# Context bar visualization (10 chars wide)
bar_width=10
filled=$(awk "BEGIN {printf \"%d\", ($context_pct / 100) * $bar_width}")
empty=$((bar_width - filled))
bar=$(printf '%*s' "$filled" '' | tr ' ' '█')$(printf '%*s' "$empty" '' | tr ' ' '░')

# Color based on context usage
if (( $(echo "$context_pct > 80" | bc -l) )); then
    color="\033[31m"  # Red
elif (( $(echo "$context_pct > 60" | bc -l) )); then
    color="\033[33m"  # Yellow
else
    color="\033[32m"  # Green
fi
reset="\033[0m"

# Output statusline
echo -e "${model} │ ${color}${bar}${reset} ${context_pct}% │ ↓${input_fmt} ↑${output_fmt}"
