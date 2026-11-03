"""PreToolUse hook: no writes to acceptance tests during implement (ADR-011@v1 C3, hard rule 3).

Reads one hook input on stdin. For a file-tool write whose target matches a glob in
acceptance-tests.json, it denies while .specify/stage reads "implement", and asks otherwise.
Anything it can't evaluate asks (Andy, 3 Nov: "fail to ask"). A crash or a missing interpreter
can't answer at all, so the hook is wired with onFailure "block". Design borrowed from
spec-gates v0.5.0 protect-files.sh: normalise the path, ignore case, resolve links, fail to ask.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
POLICY = os.path.join(ROOT, ".claude", "hooks", "acceptance-tests.json")
MARKER = os.path.join(ROOT, ".specify", "stage")


def glob_to_regex(glob):
    """Gitignore-style: ** spans folders, * and ? stay within one."""
    out, i = "", 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif glob.startswith("**", i):
            out, i = out + ".*", i + 2
        elif glob[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif glob[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(glob[i]), i + 1
    return re.compile(out + r"\Z")


def norm(path):
    """Real path with forward slashes, in the file system's case."""
    return os.path.normcase(os.path.realpath(path)).replace("\\", "/")


def decide(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason,
    }}))
    sys.exit(0)


def main():
    event = json.loads(sys.stdin.read())
    tool_input = event.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not target:
        return
    if not os.path.isabs(target):
        target = os.path.join(event.get("cwd") or os.getcwd(), target)
    target, root = norm(target), norm(ROOT)
    if not target.startswith(root + "/"):
        return
    rel = target[len(root) + 1:]

    with open(POLICY, encoding="utf-8") as f:
        globs = json.load(f)["globs"]
    if not any(glob_to_regex(os.path.normcase(g).replace("\\", "/")).match(rel) for g in globs):
        return

    stage = ""
    if os.path.exists(MARKER):
        with open(MARKER, encoding="utf-8") as f:
            stage = f.read().strip().lower()
    if stage == "implement":
        decide("deny", f"{rel} is an acceptance test, and the stage is implement. "
                       "Acceptance tests are never edited to make them pass (hard rule 3). "
                       "Report the failing test instead.")
    decide("ask", f"{rel} is an acceptance test. Confirm this change outside implement "
                  f"(stage: {stage or 'not set'}).")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # fail to ask (Andy, 3 Nov): what can't be evaluated goes to a human
        decide("ask", f"The acceptance-test hook could not evaluate this call ({e!r}). "
                      "Confirm it does not edit an acceptance test.")
