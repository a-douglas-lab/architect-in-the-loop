#!/usr/bin/env bash
# Prepare a clone or worktree: fetch the pinned subject system and check prerequisites.
# Safe to run repeatedly. Run from anywhere inside the repository.
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
cd "$root"

echo "== Subject system (eShop fork, pinned by submodule)"
git submodule update --init --recursive
echo "subject/eshop at $(git -C subject/eshop rev-parse --short HEAD)"

echo "== Private evaluation material must not be present"
if find . -path ./subject -prune -o -iname '*private-eval*' -print | grep -q .; then
  echo "ERROR: found private evaluation material in this working tree. Remove it." >&2
  exit 1
fi
echo "none found"

echo "== Prerequisites"
missing=0
check() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "ok       $1 ($($2 2>&1 | head -n 1))"
  else
    echo "MISSING  $1: $3"
    missing=1
  fi
}
check dotnet "dotnet --version" "install the SDK named in subject/eshop/global.json"
check docker "docker --version" "Aspire needs a container runtime (Docker or Podman) to run eShop"
check node   "node --version"   "needed for the capability's React frontend"

if command -v dotnet >/dev/null 2>&1; then
  required="$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' subject/eshop/global.json | head -n 1)"
  if dotnet --list-sdks | grep -q "^${required%??}"; then
    echo "ok       .NET SDK feature band for ${required}"
  else
    echo "MISSING  .NET SDK ${required} (from subject/eshop/global.json)"
    missing=1
  fi
fi

if [ "$missing" -ne 0 ]; then
  echo "Bootstrap finished with missing prerequisites (see above)."
  exit 2
fi
echo "Bootstrap complete."
