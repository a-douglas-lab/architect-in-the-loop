"""Cases T1 to T9 in expected.md, for scripts/check-trailers.py. Usage: python -I tests/ci/test_trailers.py

Each case builds a throwaway git repository in a temporary folder.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts", "check-trailers.py")
OPUS = "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"


def git(repo, *args):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com"}
    subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, env=env)


def commit(repo, name, message):
    with open(os.path.join(repo, name), "w") as f:
        f.write(name)
    git(repo, "add", name)
    git(repo, "commit", "-q", "-m", message)


def case(branch, build):
    repo = tempfile.mkdtemp()
    git(repo, "init", "-q", "-b", "main")
    commit(repo, "base.txt", "base")
    git(repo, "switch", "-q", "-c", branch)
    build(repo)
    # The base is main's tip, as CI passes the pull request's base commit. Run 1 used the
    # original branch point, which put T6's main-side commit in range (a harness fault).
    r = subprocess.run([sys.executable, "-I", SCRIPT, "main", "HEAD", branch], cwd=repo,
                       capture_output=True, text=True)
    shutil.rmtree(repo, ignore_errors=True)
    return ("pass" if r.returncode == 0 else "fail" if r.returncode == 1 else f"exit {r.returncode}"), r.stderr


def t6(repo):
    commit(repo, "a.txt", f"a\n\n{OPUS}")
    git(repo, "switch", "-q", "main")
    commit(repo, "m.txt", "on main")
    git(repo, "switch", "-q", "claude/x")
    git(repo, "merge", "-q", "--no-ff", "-m", "Merge main", "main")


CASES = [
    ("T1", "claude/x", lambda r: (commit(r, "a.txt", f"a\n\n{OPUS}"), commit(r, "b.txt", f"b\n\n{OPUS}")), "pass", None),
    ("T2", "claude/x", lambda r: (commit(r, "a.txt", f"a\n\n{OPUS}"), commit(r, "b.txt", "second, unmarked")), "fail",
     "second, unmarked"),
    ("T3", "andy/x", lambda r: commit(r, "a.txt", "by hand"), "pass", None),
    ("T4", "claude/x", lambda r: commit(r, "a.txt", "a\n\nco-authored-by: Claude Sonnet 5.5 <noreply@anthropic.com>"),
     "pass", None),
    ("T5", "claude/x", lambda r: commit(r, "a.txt", "a\n\nCo-Authored-By: Jane Doe <jane@example.com>"), "fail", None),
    ("T6", "claude/x", t6, "pass", None),
    ("T7", "claude/x", lambda r: commit(r, "a.txt", "a\n\nWritten with Claude, but no trailer.\n\nMore text."),
     "fail", None),
    ("T8", "claude/x", lambda r: None, "pass", None),
    ("T9", "claude/x", lambda r: commit(r, "a.txt", "a\n\nCo-Authored-By: Claudette Smith <c@example.com>"),
     "fail", None),
]


def main():
    fails = 0
    for cid, branch, build, want, named in CASES:
        got, err = case(branch, build)
        # A failure names the short SHA and the subject (dated expectation, 4 Nov)
        ok = got == want and (named is None or re.search(r"\b[0-9a-f]{7,} " + re.escape(named), err))
        fails += not ok
        print(f"{cid} {got}, expected {want}{' naming ' + repr(named) if named else ''}: {'pass' if ok else 'FAIL'}")
    print(f"failures: {fails}")
    return fails


if __name__ == "__main__":
    sys.exit(main())
