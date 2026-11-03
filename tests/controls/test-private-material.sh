#!/usr/bin/env bash
# Cases G1 to G10 in expected.md, for scripts/check-private-material.sh.
# Each case builds a throwaway tree under a fresh temporary folder. Usage: test-private-material.sh [--old]
# --old runs the guard as it was in scripts/bootstrap.sh at 2732f29, lines 14 to 17, to show the gap.
set -uo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
guard="$here/../../scripts/check-private-material.sh"
url='https://github.com/a-douglas-lab/Architect-in-the-loop-evaluator.git'

old_guard() {
  cd "$1" && if find . -path ./subject -prune -o -iname '*private-eval*' -print | grep -q .; then return 1; fi
}

build() {  # build <case> <root>
  local r="$2"
  mkdir -p "$r/docs" "$r/subject/eshop/src"
  case "$1" in
    G2) mkdir "$r/Architect-in-the-loop-evaluator" ;;
    G3) mkdir -p "$r/docs/x/architect-in-the-loop-EVALUATOR" ;;
    G4) mkdir "$r/subject/Architect-in-the-loop-evaluator" ;;
    G5) mkdir "$r/subject/private-eval" ;;
    G6) mkdir "$r/private-eval" ;;
    G7) : > "$r/Architect-in-the-loop-evaluator.zip" ;;
    G8) mkdir -p "$r/scratch/.git" && printf '[remote "origin"]\n\turl = %s\n' "$url" > "$r/scratch/.git/config" ;;
    G9) printf '[submodule "x"]\n\tpath = x\n\turl = %s\n' "$url" > "$r/.gitmodules" ;;
    G10) mkdir -p "$r/evaluator" "$r/Architect-in-the-loop" "$r/grader-evaluation" "$r/other/.git" &&
         printf '[remote "origin"]\n\turl = https://github.com/dotnet/eShop.git\n' > "$r/other/.git/config" ;;
  esac
}

declare -A want=([G1]=0 [G2]=1 [G3]=1 [G4]=1 [G5]=1 [G6]=1 [G7]=1 [G8]=1 [G9]=1 [G10]=0)
fails=0
for c in G1 G2 G3 G4 G5 G6 G7 G8 G9 G10; do
  root="$(mktemp -d)"
  build "$c" "$root"
  if [ "${1:-}" = "--old" ]; then
    (old_guard "$root") >/dev/null 2>&1; got=$?
    echo "$c old guard: exit $got"
  else
    bash "$guard" "$root" >/dev/null 2>&1; got=$?
    if [ "$got" = "${want[$c]}" ]; then r=pass; else r=FAIL; fails=$((fails + 1)); fi
    echo "$c exit $got, expected ${want[$c]}: $r"
  fi
  rm -rf "$root"
done
[ "${1:-}" = "--old" ] || echo "failures: $fails"
exit $fails
