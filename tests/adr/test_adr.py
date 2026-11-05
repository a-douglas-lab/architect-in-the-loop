"""Cases A0 to A19 in expected.md, for scripts/adr.py. Usage: python -I tests/adr/test_adr.py

Each case copies docs/adr/, the constitution, CLAUDE.md and scripts/adr.py into a throwaway git
repository, commits that as the base, applies one change, commits it, and runs check --base.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ADR5 = "docs/adr/" + next(n for n in os.listdir(os.path.join(REPO, "docs", "adr")) if n.startswith("ADR-005-"))


def git(repo, *args):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com"}
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True, env=env)


def make_repo():
    repo = tempfile.mkdtemp()
    shutil.copytree(os.path.join(REPO, "docs", "adr"), os.path.join(repo, "docs", "adr"))
    os.makedirs(os.path.join(repo, ".specify", "memory"))
    shutil.copy(os.path.join(REPO, ".specify", "memory", "constitution.md"), os.path.join(repo, ".specify", "memory"))
    shutil.copy(os.path.join(REPO, "CLAUDE.md"), repo)
    os.makedirs(os.path.join(repo, "scripts"))
    for name in ("adr.py", "adr-front-matter.schema.json"):
        shutil.copy(os.path.join(REPO, "scripts", name), os.path.join(repo, "scripts"))
    git(repo, "init", "-q", "-b", "main")
    git(repo, "-c", "core.autocrlf=false", "add", "-A")
    git(repo, "commit", "-q", "-m", "base")
    return repo


def edit(repo, rel, fn):
    path = os.path.join(repo, rel)
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    new = fn(text)
    assert new != text, f"mutation of {rel} changed nothing"
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new)


def sub(pattern, repl, count=1, flags=re.M | re.S):
    return lambda t: re.sub(pattern, repl, t, count=count, flags=flags)


def section_swap(t):
    cons = re.search(r"^## Consequences\n.*?(?=^## Alternatives)", t, re.M | re.S).group(0)
    alts = re.search(r"^## Alternatives\n.*?(?=^## Enforcement)", t, re.M | re.S).group(0)
    return t.replace(cons + alts, alts + cons)


def bump(t):
    t = t.replace("version: 3\n", "version: 4\n", 1)
    return t.rstrip("\n") + "\n- **v4** · 2026-11-04 · revision · approved by Andy Douglas in chat: test.\n"


def bump_with(kind):
    return lambda t: bump(t).replace("· revision · approved by Andy Douglas in chat: test.", f"· {kind} · test.")


DECISION_WORD = sub(r"(^## Decision\n\n\S+)", r"\1X")
NEW_ADR = """---
id: ADR-099
version: 1
title: A test decision
status: accepted
date: 2026-11-04
decision-makers: [Andy Douglas]
scope: [project]
precedence:
  tier: cross-cutting
  overrides: []
supersedes: []
superseded-by: null
exceptions: not-allowed
enforcement:
  - constraint: C1
    mechanism: review
    ref: null
    state: manual
backlog: []
---

# ADR-099: A test decision

## Context

Test.

## Decision

Test.

## Constraints

- **C1:** Tests MUST pass.

## Consequences

None.

## Alternatives

None.

## Enforcement

Review.

## History

- **v1** · 2026-11-04 · accepted · Andy Douglas: first version.
"""


def add_file(rel, text):
    def go(repo):
        with open(os.path.join(repo, rel), "w", encoding="utf-8", newline="") as f:
            f.write(text)
    return go


def rename(repo):
    git(repo, "mv", ADR5, ADR5.replace("ADR-005-", "ADR-050-"))


def write_index(repo):
    subprocess.run([sys.executable, "-I", os.path.join(repo, "scripts", "adr.py"), "index", "--write"], check=True)


CASES = [  # id, list of changes (callables on repo), expected ("pass" or "fail"), rules expected in output
    ("A0", [], "pass", []),
    ("A1", [lambda r: edit(r, ADR5, sub(r"^## Alternatives\n.*?(?=^## Enforcement)", ""))], "fail", ["C2"]),
    ("A2", [lambda r: edit(r, ADR5, section_swap)], "fail", ["C2"]),
    ("A3", [rename], "fail", ["C3"]),
    ("A4", [lambda r: edit(r, "docs/adr/" + [n for n in os.listdir(os.path.join(r, "docs/adr")) if n.startswith("ADR-006")][0],
                           sub(r"^id: ADR-006$", "id: ADR-005"))], "fail", ["C3: id ADR-005 is used by", "doesn't start with its id"]),
    ("A5", [lambda r: edit(r, ADR5, sub(r"^id: ADR-005$", "id: ADR-5"))], "fail", ["C3"]),
    ("A6", [lambda r: edit(r, ADR5, sub(r"(^- \*\*C7:\*\*.*?$)", r"\1\n- **C99:** Tests MUST pass."))], "fail", ["C5"]),
    ("A7", [lambda r: edit(r, ADR5, sub(r"(^backlog:)", "  - constraint: C99\n    mechanism: review\n    ref: null\n    state: manual\n\\1"))],
     "fail", ["C5"]),
    ("A8", [lambda r: edit(r, ADR5, DECISION_WORD)], "fail", ["C8"]),
    ("A9", [lambda r: edit(r, ADR5, lambda t: DECISION_WORD(t).replace("version: 3\n", "version: 4\n", 1))], "fail", ["C8"]),
    ("A10", [lambda r: edit(r, ADR5, lambda t: bump(DECISION_WORD(t)))], "pass", []),
    ("A11", [lambda r: edit(r, ADR5, sub(r"(constraint: C7\n.*?state: )\w+", r"\1enforced"))], "pass", []),
    ("A12", [lambda r: edit(r, ADR5, lambda t: re.sub(r"  - constraint: C7\n(    .*\n){3}", "",
                                                      re.sub(r"^- \*\*C7:\*\*.*\n", "", bump(DECISION_WORD(t)), flags=re.M)))],
     "fail", ["C9"]),
    ("A13", [lambda r: edit(r, ADR5, lambda t: re.sub(r"(constraint: C7\n(?:    .*\n){2}    state: )\w+", r"\1withdrawn",
                                                      re.sub(r"^(- \*\*C7:\*\*).*$", r"\1 *Withdrawn in v4.*",
                                                             bump(DECISION_WORD(t)), flags=re.M)))], "pass", []),
    ("A14", [lambda r: edit(r, ".specify/memory/constitution.md", sub(r"(^\| \[ADR-005\]\([^)]*\) \| )", r"\1Changed "))],
     "fail", ["C10, C14"]),
    ("A15", [lambda r: edit(r, ".specify/memory/constitution.md", sub(r"^\| \[ADR-005\].*\n", ""))], "fail", ["C10, C14"]),
    ("A16", [add_file("docs/adr/ADR-099-test.md", NEW_ADR)], "fail", ["C10, C14"]),
    ("A17", [add_file("docs/adr/ADR-099-test.md", NEW_ADR), write_index], "pass", []),
    ("A18", [lambda r: edit(r, ".specify/memory/constitution.md", sub(r"^(3\. \*\*Never edit acceptance tests)", r"\1 ever"))],
     "fail", ["C17"]),
    ("A19", [lambda r: edit(r, ADR5, lambda t: bump_with("update")(DECISION_WORD(t)))], "fail", ["C8"]),
    # A20-A25: dated expectations after review run 1 (4 Nov)
    ("A20", [lambda r: edit(r, ADR5, lambda t: re.sub(r"^(- \*\*C7:\*\*).*$", r"\1 *Withdrawn in v4.*",
                                                      bump(DECISION_WORD(t)), flags=re.M))], "fail", ["C9"]),
    ("A21", [lambda r: edit(r, ADR5, lambda t: re.sub(r"(constraint: C7\n(?:    .*\n){2}    state: )\w+", r"\1withdrawn",
                                                      bump(DECISION_WORD(t))))], "fail", ["C9"]),
    ("A22", [lambda r: edit(r, ADR5, lambda t: bump(DECISION_WORD(t)).replace("version: 4\n", "version: 5\n", 1)
                                                .replace("- **v4** ·", "- **v5** ·"))], "fail", ["C8"]),
    ("A23", [lambda r: edit(r, ADR5, lambda t: DECISION_WORD(t).replace("version: 3\n", "version: 4\n", 1).rstrip("\n")
                            + "\n- **v4** · 2026-11-04 · revision · x\n")], "fail", ["C8"]),
    ("A24", [lambda r: edit(r, "CLAUDE.md", sub(r"^## Hard rules$", "## Rules"))], "fail", ["C17"]),
    # A25 regenerates the index after the change, so only the YAML cross-check can catch it (review run 2:
    # without this, the old index message also contained "C14" and the new check went untested)
    ("A25", [lambda r: edit(r, ADR5, sub(r"^scope: \[project, subject, domain:ordering\]$",
                                         "scope:\n  - project\n  - subject\n  - domain:ordering")), write_index],
     "fail", ["reads differently as YAML"]),
    # F: front-matter schema (dated expectation, 4 Nov). Front-matter-only edits of an accepted ADR
    # also break C8 against the base, so F cases compare with HEAD itself (base = the change).
    ("F0", [], "pass", []),
    ("F1", [lambda r: edit(r, ADR5, sub(r"^backlog:.*\n", ""))], "fail", ["C1"]),
    ("F2", [lambda r: edit(r, ADR5, sub(r"^status: accepted$", "status: approved"))], "fail", ["C1"]),
    ("F3", [lambda r: edit(r, ADR5, sub(r"^version: 3$", "version: two"))], "fail", ["C1"]),
    ("F4", [lambda r: edit(r, ADR5, sub(r"^date: .*$", "date: 4 Nov 2026"))], "fail", ["C1"]),
    ("F5", [lambda r: edit(r, ADR5, sub(r"(constraint: C7\n(?:    .*\n){2}    state: )\w+", r"\1done"))], "fail", ["C1"]),
    ("F6", [lambda r: edit(r, ADR5, sub(r"^  overrides:.*\n", ""))], "fail", ["C1"]),
    ("F7", [lambda r: edit(r, ADR5, sub(r"^superseded-by: .*$", "superseded-by: ADR-5"))], "fail", ["C1"]),
    ("F8", [lambda r: edit(r, ADR5, sub(r"^scope: .*$", "scope: project"))], "fail", ["C1"]),
    ("F9", [lambda r: edit(r, ADR5, sub(r"^scope: \[", "scope: [[", ))], "fail", ["C1"]),
    ("F10", [lambda r: edit(r, ADR5, sub(r"^(backlog:.*)$", r"\1\nowner: Andy Douglas"))], "pass", []),
]


def main():
    fails = 0
    for cid, changes, want, rules in CASES:
        repo = make_repo()
        for change in changes:
            change(repo)
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "--allow-empty", "-m", cid)
        base = "HEAD" if cid.startswith("F") else "HEAD~1"
        r = subprocess.run([sys.executable, "-I", os.path.join(repo, "scripts", "adr.py"), "check", "--base", base],
                           cwd=repo, capture_output=True, text=True, encoding="utf-8")
        got = "pass" if r.returncode == 0 else "fail" if r.returncode == 1 else f"exit {r.returncode}"
        ok = got == want and all(rule in r.stderr for rule in rules)
        # Tightened after review run 1: F must fail on the schema itself, not on missing libraries,
        # and A16's new ADR must not be compared for C8
        if cid.startswith("F") and "not checked" in r.stderr:
            ok = False
        if cid == "A16" and "ADR-099-test.md: C8" in r.stderr:
            ok = False
        fails += not ok
        print(f"{cid} {got}, expected {want} {rules or ''}: {'pass' if ok else 'FAIL'}")
        if not ok:
            print("   " + (r.stderr.strip() or r.stdout.strip()).replace("\n", "\n   "))
        shutil.rmtree(repo, ignore_errors=True)
    print(f"failures: {fails}")
    return fails


if __name__ == "__main__":
    sys.exit(main())
