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

if command -v npx &>/dev/null; then
  echo "--- Playwright browsers ---"
  echo "Close Playwright browsers and MCP sessions first."
  if read -r -p "Uninstall all downloaded Playwright browsers? [y/N] " reply && [[ "$reply" =~ ^[Yy]$ ]]; then
    npx --yes playwright@1.63.0 uninstall --all
  fi
  echo
fi

if command -v npm &>/dev/null; then
  echo "--- npm and npx caches ---"
  npm cache clean --force
  npm cache npx rm --force
  echo
fi

if command -v fnm &>/dev/null; then
  echo "--- Installed fnm Node versions ---"
  fnm list
  echo "Remove unwanted versions manually with: fnm uninstall <version>"
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
