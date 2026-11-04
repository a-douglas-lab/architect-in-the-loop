"""Cases D1 to D5 in expected.md, for scripts/check-changed.py. Usage: python -I tests/ci/test_changed.py

Each case builds a throwaway git repository holding copies of the hooks and the script.
"""
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def git(repo, *args):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com"}
    subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, env=env)


def write(repo, rel, content):
    path = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def make_repo():
    repo = tempfile.mkdtemp()
    git(repo, "init", "-q", "-b", "main")
    for name in ("check_edited.py", "acceptance_tests.py", "acceptance-tests.json"):
        os.makedirs(os.path.join(repo, ".claude", "hooks"), exist_ok=True)
        shutil.copy(os.path.join(REPO, ".claude", "hooks", name), os.path.join(repo, ".claude", "hooks", name))
    os.makedirs(os.path.join(repo, "scripts"))
    shutil.copy(os.path.join(REPO, "scripts", "check-changed.py"), os.path.join(repo, "scripts"))
    write(repo, "old.json", '{"a": 1}')
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "base")
    git(repo, "switch", "-q", "-c", "claude/x")
    return repo


def d4(repo):
    os.remove(os.path.join(repo, "old.json"))


CASES = [  # id, change, expected, text expected in output
    ("D1", lambda r: (write(r, "a.json", '{"ok": true}'), write(r, "b.py", "x = 1\n")), "pass", None),
    ("D2", lambda r: write(r, "config/bad.json", '{"a": 1,'), "fail", "config/bad.json"),
    ("D3", lambda r: write(r, "tests/acceptance/OrderTests.cs", "// test\n"), "pass",
     "acceptance-test change (reported, not failed): tests/acceptance/OrderTests.cs"),
    ("D4", d4, "pass", None),
    ("D5", lambda r: write(r, "notes.md", "# not checked {\n"), "pass", None),
]


def main():
    fails = 0
    for cid, change, want, text in CASES:
        repo = make_repo()
        change(repo)
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", cid)
        r = subprocess.run([sys.executable, "-I", os.path.join(repo, "scripts", "check-changed.py"), "main", "HEAD"],
                           cwd=repo, capture_output=True, text=True)
        got = "pass" if r.returncode == 0 else "fail" if r.returncode == 1 else f"exit {r.returncode}"
        ok = got == want and (text is None or text in r.stdout + r.stderr)
        fails += not ok
        print(f"{cid} {got}, expected {want}: {'pass' if ok else 'FAIL'}")
        if not ok:
            print(r.stdout + r.stderr)
        shutil.rmtree(repo, ignore_errors=True)
    print(f"failures: {fails}")
    return fails


if __name__ == "__main__":
    sys.exit(main())
