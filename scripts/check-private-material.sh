#!/usr/bin/env bash
# Fail if private evaluation material is in a working tree (CLAUDE.md hard rule 1, ADR-011@v1 C7).
# Matches names anywhere in the tree, subject/ included, and remote URLs in git files.
# Reads only names and git metadata inside the tree. Usage: check-private-material.sh [root]
set -euo pipefail

root="${1:-$(git rev-parse --show-toplevel)}"
pattern='private-eval|architect-in-the-loop-evaluator'

# Any file or folder whose name matches, in any case.
found="$(find "$root" \( -iname '*private-eval*' -o -iname '*architect-in-the-loop-evaluator*' \) -print)"

# A clone or submodule under another name still records its remote URL.
urls="$(find "$root" \( -name .gitmodules -o -name .git -type f -o -path '*/.git/config' -o -path '*/.git/modules/*/config' \) -type f -print0 \
  | xargs -0 -r grep -liE "$pattern" || true)"

if [ -n "$found$urls" ]; then
  echo "ERROR: found private evaluation material in this working tree. Remove it:" >&2
  printf '%s\n%s\n' "$found" "$urls" | sed '/^$/d' >&2
  exit 1
fi
echo "none found"
