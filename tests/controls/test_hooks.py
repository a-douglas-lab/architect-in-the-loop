"""Cases H1 to H15 and K1 to K10 in expected.md. Usage: python -I tests/controls/test_hooks.py

Each case copies the hooks into a throwaway root, pipes one hook input on stdin, and
compares the outcome with the expected one. Nothing outside the temporary folder is touched.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HOOKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".claude", "hooks")


def make_root():
    root = tempfile.mkdtemp()
    os.makedirs(os.path.join(root, ".claude", "hooks"))
    os.makedirs(os.path.join(root, ".specify"))
    os.makedirs(os.path.join(root, "tests"))
    for name in ("acceptance_tests.py", "acceptance-tests.json", "check_edited.py"):
        shutil.copy(os.path.join(HOOKS, name), os.path.join(root, ".claude", "hooks", name))
    os.makedirs(os.path.join(root, "scripts"))  # the ADR validator, which check_edited.py calls (tests/adr K12-K14)
    shutil.copy(os.path.join(HOOKS, "..", "..", "scripts", "adr.py"), os.path.join(root, "scripts"))
    return root


ADR_DIR = os.path.join(HOOKS, "..", "..", "docs", "adr")
ADR5_TEXT = open(os.path.join(ADR_DIR, next(n for n in os.listdir(ADR_DIR) if n.startswith("ADR-005-"))),
                 encoding="utf-8").read()
TEMPLATE_TEXT = open(os.path.join(ADR_DIR, "template.md"), encoding="utf-8").read()


def run(root, hook, stdin, env=None):
    r = subprocess.run([sys.executable, "-I", os.path.join(root, ".claude", "hooks", hook)],
                       input=stdin, capture_output=True, text=True, env=env)
    if r.returncode == 2:
        return "blocked"
    if r.returncode != 0:
        return f"exit {r.returncode}"
    if not r.stdout.strip():
        return "none"
    out = json.loads(r.stdout)
    if "hookSpecificOutput" in out:
        return out["hookSpecificOutput"]["permissionDecision"]
    if out.get("decision") == "block":
        return "reported: " + out.get("reason", "")
    return "silent"


def event(root, tool, path, key="file_path", cwd=None):
    return json.dumps({"hook_event_name": "PreToolUse", "tool_name": tool, "cwd": cwd or root,
                       "tool_input": {key: path}})


def h_cases():
    acc = "tests/acceptance/OrderTests.cs"
    win = "{root}\\subject\\eshop\\tests\\Ordering.AcceptanceTests\\X.cs"
    return [  # id, tool, path, key, stage, cwd suffix, setup, expected
        ("H1", "Write", acc, "file_path", "implement", None, None, "deny"),
        ("H2", "Edit", acc, "file_path", "implement", None, None, "deny"),
        ("H3", "NotebookEdit", "tests/acceptance/n.ipynb", "notebook_path", "implement", None, None, "deny"),
        ("H4", "Write", acc, "file_path", None, None, None, "ask"),
        ("H5", "Write", acc, "file_path", "specify", None, None, "ask"),
        ("H6", "Write", "src/Ordering/Order.cs", "file_path", "implement", None, None, "none"),
        ("H7", "Write", win, "file_path", "implement", None, None, "deny"),
        ("H8", "Write", "Tests/Acceptance/x.cs", "file_path", "implement", None, None,
         "deny" if os.name == "nt" else "none"),
        ("H9", "Write", "src/../tests/acceptance/x.cs", "file_path", "implement", None, None, "deny"),
        ("H10", "Write", "acceptance/x.cs", "file_path", "implement", "tests", None, "deny"),
        # H11, H12: "blocked" until Andy's ruling of 3 Nov, "fail to ask" (dated expectation)
        ("H11", None, None, None, "implement", None, None, "ask"),
        ("H12", "Write", acc, "file_path", "implement", None, "no-policy", "ask"),
        ("H13", "Write", "{outside}/tests/acceptance/x.cs", "file_path", "implement", None, None, "none"),
        ("H14", "Write", acc, "file_path", "Implement\n", None, None, "deny"),
        ("H15", "MultiEdit", acc, "file_path", "implement", None, None, "deny"),
    ]


def k_cases():
    return [  # id, file name, content, expected
        ("K1", "a.json", '{"a": 1}', "silent"),
        ("K2", "b.json", '{"a": 1,', "reported"),
        ("K3", "c.py", "x = 1\n", "silent"),
        ("K4", "d.py", "def f(:\n", "reported"),
        ("K5", "e.sh", "echo ok\n", "silent"),
        ("K6", "f.sh", "if then fi\n", "reported"),
        ("K7", "g.ps1", "Write-Host 'ok'\n", "silent"),
        ("K8", "h.ps1", "function f( {\n", "reported"),
        ("K9", "i.md", "# not checked {\n", "silent"),
        ("K10", None, None, "silent"),
        ("K11", "j.ps1", "Write-Host 'ok'\n", "reported"),  # no PowerShell on PATH (tests/ci, 4 Nov)
        # K12-K14: ADR edits (tests/adr/expected.md, 4 Nov)
        ("K12", "docs/adr/ADR-005-x.md", re.sub(r"^## Alternatives\n.*?(?=^## Enforcement)", "", ADR5_TEXT,
                                                 flags=re.M | re.S), "reported"),
        ("K13", "docs/adr/ADR-005-x.md", ADR5_TEXT, "silent"),
        ("K14", "docs/adr/template.md", TEMPLATE_TEXT, "silent"),
    ]


def main():
    fails = 0
    outside = tempfile.mkdtemp()
    for cid, tool, path, key, stage, cwd, setup, want in h_cases():
        root = make_root()
        if stage is not None:
            with open(os.path.join(root, ".specify", "stage"), "w", encoding="utf-8") as f:
                f.write(stage)
        if setup == "no-policy":
            os.remove(os.path.join(root, ".claude", "hooks", "acceptance-tests.json"))
        if tool is None:
            stdin = "this is not json"
        else:
            path = path.format(root=root, outside=outside)
            stdin = event(root, tool, path, key, os.path.join(root, cwd) if cwd else None)
        got = run(root, "acceptance_tests.py", stdin)
        ok = got == want
        fails += not ok
        print(f"{cid} {got}, expected {want}: {'pass' if ok else 'FAIL'}")
        shutil.rmtree(root)
    for cid, name, content, want in k_cases():
        root = make_root()
        path = os.path.join(root, name or "gone.json")
        if name:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        stdin = json.dumps({"hook_event_name": "PostToolUse", "tool_name": "Write", "cwd": root,
                            "tool_input": {"file_path": path}, "tool_response": {}})
        # K11: PATH holds only an empty folder, so neither powershell nor pwsh is found
        env = {**os.environ, "PATH": root} if cid == "K11" else None
        got = run(root, "check_edited.py", stdin, env)
        got = "silent" if got == "none" else got
        # K12 must name the rule it breaks (tests/adr/expected.md); other cases compare the outcome only
        if got.startswith("reported: ") and not (cid == "K12" and "C2" not in got):
            got = "reported"
        ok = got == want
        fails += not ok
        print(f"{cid} {got}, expected {want}: {'pass' if ok else 'FAIL'}")
        shutil.rmtree(root)
    shutil.rmtree(outside)
    print(f"failures: {fails}")
    return fails


if __name__ == "__main__":
    sys.exit(main())
