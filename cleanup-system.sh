#!/usr/bin/env bash
set -euo pipefail

echo "=== System Cleanup ==="
echo

before=$(df -h / | tail -1 | awk '{print $4}')
echo "Free space before: $before"
echo

if command -v uv &>/dev/null; then
  echo "--- uv cache ---"
  uv cache clean
  echo
fi

if command -v pnpm &>/dev/null; then
  echo "--- pnpm store ---"
  pnpm store prune
  echo
fi

if command -v npm &>/dev/null; then
  echo "--- npm cache ---"
  npm cache clean --force
  echo
fi

if command -v brew &>/dev/null; then
  echo "--- Homebrew ---"
  brew cleanup --prune=all
  echo
fi

if command -v docker &>/dev/null; then
  echo "--- Docker ---"
  docker system prune -a --volumes -f
  echo
fi

after=$(df -h / | tail -1 | awk '{print $4}')
echo "=== Done ==="
echo "Free space before: $before"
echo "Free space after:  $after"
