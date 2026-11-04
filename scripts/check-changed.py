"""Run the controls' rules on a pull request's changed files (backlog Q6, VL-6; Andy, 4 Nov).

Usage: python -I scripts/check-changed.py <base> <head>
Each file added or changed in base..head that still exists gets the C1 hook's own check
(check() in .claude/hooks/check_edited.py: one definition, VL-1). Any failure fails the run.
Changes to the C3 acceptance-test globs are listed, not failed: CI can't tell implement from
the stage that writes tests ("C1 check + guard; C3 reported").
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                      check=True).stdout.strip()
HOOKS = os.path.join(ROOT, ".claude", "hooks")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HOOKS, f"{name}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(base, head):
    check_edited, acceptance = load("check_edited"), load("acceptance_tests")
    with open(os.path.join(HOOKS, "acceptance-tests.json"), encoding="utf-8") as f:
        globs = [acceptance.glob_to_regex(g) for g in json.load(f)["globs"]]
    changed = subprocess.run(["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...{head}"],
                             capture_output=True, text=True, check=True, cwd=ROOT).stdout.split()
    failures, acceptance_changes = [], []
    for rel in changed:
        if any(g.match(rel) for g in globs):
            acceptance_changes.append(rel)
        path = os.path.join(ROOT, rel)
        if os.path.isfile(path):
            error = check_edited.check(path)
            if error:
                failures.append(f"{rel}: {error}")
    for rel in acceptance_changes:
        print(f"acceptance-test change (reported, not failed): {rel}")
    for line in failures:
        print(f"fails its check: {line}", file=sys.stderr)
    print(f"{len(changed)} changed files checked, {len(failures)} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
