"""PostToolUse hook: syntax-check a file after Claude edits it (ADR-011@v1 C1, as far as it goes today).

The repository has no build or formatter yet, so this checks what it can by file type and
reports a failure next to the tool result, for Claude to fix. It never blocks: the edit has
already happened. When the capability has code, its build and format join here.
"""
import json
import os
import shutil
import subprocess
import sys


def find_bash():
    """Git Bash on Windows, where only git's cmd folder may be on PATH; bash elsewhere."""
    if os.name == "nt":
        git = shutil.which("git")
        if git:
            bash = os.path.join(os.path.dirname(os.path.dirname(git)), "bin", "bash.exe")
            if os.path.isfile(bash):
                return bash
    return shutil.which("bash")


def check(path):
    """Return an error message, or None if the file passes or has no check."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        try:
            with open(path, encoding="utf-8-sig") as f:
                json.load(f)
        except ValueError as e:
            return str(e)
    elif ext == ".py":
        try:  # compile() rather than py_compile, which would write a .pyc into the tree
            with open(path, "rb") as f:
                compile(f.read(), path, "exec")
        except (SyntaxError, ValueError) as e:
            return str(e)
    elif ext == ".sh":
        bash = find_bash()
        if not bash:
            return "no bash found to check it with"
        r = subprocess.run([bash, "-n", path], capture_output=True, text=True)
        if r.returncode:
            return r.stderr.strip()
    elif ext == ".ps1":
        script = ("$e = $null; [void][System.Management.Automation.Language.Parser]::ParseFile("
                  "$env:CHECK_PATH, [ref]$null, [ref]$e); $e | ForEach-Object { $_.ToString() }")
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                           capture_output=True, text=True, env={**os.environ, "CHECK_PATH": path})
        if r.stdout.strip():
            return r.stdout.strip()
    return None


def main():
    event = json.loads(sys.stdin.read())
    tool_input = event.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not path:
        return
    if not os.path.isabs(path):
        path = os.path.join(event.get("cwd") or os.getcwd(), path)
    if not os.path.isfile(path):
        return
    error = check(path)
    if error:
        print(json.dumps({"decision": "block",
                          "reason": f"check_edited: {path} fails its syntax check: {error}"}))


if __name__ == "__main__":
    main()
