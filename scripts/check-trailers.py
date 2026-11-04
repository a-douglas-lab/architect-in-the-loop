"""Check that AI-authored commits carry a Co-Authored-By: Claude trailer (ADR-010@v1 C5).

Usage: python -I scripts/check-trailers.py <base> <head> <branch>
On a branch named claude/*, every commit in base..head that isn't a merge must carry a
Co-Authored-By trailer (any case, as git reads trailers) whose value names Claude as a word.
Other branches aren't checked: CI can't tell an AI-authored commit by itself. Merge commits
are skipped (both Andy, 4 Nov).
"""
import re
import subprocess
import sys


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def main(base, head, branch):
    if not branch.startswith("claude/"):
        print(f"{branch}: not a claude/* branch, not checked")
        return 0
    missing = []
    for sha in git("rev-list", "--no-merges", f"{base}..{head}").split():
        values = git("log", "-1", "--format=%(trailers:key=Co-Authored-By,valueonly)", sha)
        if not any(re.search(r"\bclaude\b", v, re.IGNORECASE) for v in values.splitlines()):
            missing.append(git("log", "-1", "--format=%h %s", sha).strip())
    for line in missing:
        print(f"missing Co-Authored-By: Claude trailer: {line}", file=sys.stderr)
    if missing:
        return 1
    print("every commit carries the trailer")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
