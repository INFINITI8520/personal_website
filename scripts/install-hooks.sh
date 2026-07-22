#!/bin/sh
# Run this once (git doesn't version hooks, so it must be installed per clone):
#   sh scripts/install-hooks.sh
set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
cp "$REPO_ROOT/scripts/hooks/pre-commit" "$REPO_ROOT/.git/hooks/pre-commit"
chmod +x "$REPO_ROOT/.git/hooks/pre-commit"

echo "Pre-commit hook installed. blog.html and projects.html will now update automatically on commit."
