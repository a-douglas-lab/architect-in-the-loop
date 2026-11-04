"""ADR validator and index generator (Step 7, item 2; backlog Q6, VL-9).

Usage:
  python -I scripts/adr.py check [--base <ref>]   check every ADR, the index and the hard rules
  python -I scripts/adr.py index [--write]        print, or rewrite, the constitution's ADR index

Checks the rules that need git and plain code: ADR-000@v3 C2, C3, C5, C8, C9 and ADR-009@v2
C10, C14, C17. The front-matter schema (ADR-000@v3 C1) waits for the CUE versus JSON Schema
research (Andy, 4 Nov: "Code checks now; CUE question researched first"), so front matter is
read with line patterns here, not a YAML parser. check_file() is also run by the C1 hook and
by CI's changed-files check on any edited ADR.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADR_DIR = "docs/adr"
CONSTITUTION = ".specify/memory/constitution.md"
SECTIONS = ["Context", "Decision", "Constraints", "Consequences", "Alternatives", "Enforcement", "History"]
ADR_FILE = re.compile(r"ADR-\d{3}-.*\.md\Z")
HISTORY = re.compile(r"^- \*\*v(\d+)\*\* · (\d{4}-\d{2}-\d{2}) · (\S+) · ", re.M)
INDEX_ROW = re.compile(r"^\| \[ADR-\d{3}\]\(.*$", re.M)


def parse(text):
    """The fields the checks need, read with line patterns (see the module docstring)."""
    m = re.match(r"---\n(.*?)\n---\n(.*)\Z", text.replace("\r\n", "\n"), re.S)
    front, body = (m.group(1), m.group(2)) if m else ("", text)

    def field(name):
        f = re.search(rf"^{name}:[ \t]*(.*)$", front, re.M)
        if not f:
            return None
        value = f.group(1).strip()
        # A YAML scalar may be quoted, as ADR-004's title is because it holds a colon
        if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1].replace('\\"', '"') if value[0] == '"' else value[1:-1].replace("''", "'")
        return value

    scope = field("scope") or ""
    sections = re.findall(r"^## (.+?)\s*$", body, re.M)
    constraints_text = re.search(r"^## Constraints\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    history_text = re.search(r"^## History\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    # front matter with each enforcement entry's state and ref removed (ADR-000@v3 C8's exception)
    comparable = re.sub(r"^\s+(state|ref):.*\n", "", front + "\n", flags=re.M) + body
    return {
        "id": field("id"), "version": field("version"), "title": field("title"),
        "scope": [s.strip() for s in scope.strip("[]").split(",") if s.strip()],
        "enforced": re.findall(r"^\s*- constraint:\s*(C\d+)\s*$", front, re.M),
        "sections": sections,
        "constraints": re.findall(r"^- \*\*(C\d+):\*\*", constraints_text.group(1) if constraints_text else "", re.M),
        "history": [(int(v), d, t) for v, d, t in HISTORY.findall(history_text.group(1) if history_text else "")],
        "comparable": comparable,
    }


def check_file(path, text):
    """Per-file rules: ADR-000@v3 C2, C3 (format and file name) and C5. Returns problems."""
    name, a, problems = os.path.basename(path), parse(text), []
    if a["sections"] != SECTIONS:
        problems.append(f"C2: sections are {a['sections']}, expected {SECTIONS}")
    if not a["id"] or not re.fullmatch(r"ADR-\d{3}", a["id"]):
        problems.append(f"C3: id {a['id']!r} isn't ADR- plus three digits")
    elif not name.startswith(a["id"] + "-"):
        problems.append(f"C3: file name {name} doesn't start with its id {a['id']}")
    listed, entries = a["constraints"], a["enforced"]
    for c in sorted(set(listed) - set(entries)):
        problems.append(f"C5: constraint {c} has no enforcement entry")
    for c in sorted(set(entries) - set(listed)):
        problems.append(f"C5: enforcement entry {c} names no constraint")
    for c in sorted({c for c in entries if entries.count(c) > 1}):
        problems.append(f"C5: constraint {c} has more than one enforcement entry")
    return [f"{path}: {p}" for p in problems]


def adr_paths():
    folder = os.path.join(ROOT, ADR_DIR)
    return sorted(f"{ADR_DIR}/{n}" for n in os.listdir(folder) if n.startswith("ADR-") and n.endswith(".md"))


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def at_base(ref, rel):
    r = subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    return r.stdout if r.returncode == 0 else None


def compare(rel, old, new):
    """ADR-000@v3 C8 and C9, against the ADR as it was at the base."""
    o, n, problems = parse(old), parse(new), []
    for c in sorted(set(o["constraints"]) - set(n["constraints"])):
        problems.append(f"C9: constraint {c} was removed; withdraw it instead")
    if o["comparable"] == n["comparable"]:
        return [f"{rel}: {p}" for p in problems]
    try:
        old_v, new_v = int(o["version"]), int(n["version"])
    except (TypeError, ValueError):
        return [f"{rel}: C8: version isn't a number"]
    if new_v <= old_v:
        problems.append(f"C8: changed, but version stayed {new_v}")
    added = [h for h in n["history"] if h[0] > old_v]
    if not added:
        problems.append("C8: changed, but no new History line")
    for v, _, kind in added:
        if kind not in ("revision", "correction"):
            problems.append(f"C8: History line v{v} has type {kind!r}, expected revision or correction")
    if added and max(h[0] for h in added) != new_v:
        problems.append(f"C8: the newest History line isn't for v{new_v}")
    return [f"{rel}: {p}" for p in problems]


def index_rows():
    rows = []
    for rel in adr_paths():
        a = parse(read(rel))
        rows.append(f"| [{a['id']}](../../{rel}) | {a['title']} | {', '.join(a['scope'])} |")
    return rows


def hard_rules():
    m = re.search(r"^## Hard rules\s*$(.*?)(?=^## |\Z)", read("CLAUDE.md"), re.M | re.S)
    return re.findall(r"^\d+\. .+$", m.group(1) if m else "", re.M)


def check(base=None):
    problems, ids = [], {}
    for rel in adr_paths():
        text = read(rel)
        problems += check_file(rel, text)
        ids.setdefault(parse(text)["id"], []).append(rel)
        if base:
            old = at_base(base, rel)
            if old is not None:
                problems += compare(rel, old, text)
    for adr_id, files in ids.items():
        if len(files) > 1:
            problems.append(f"C3: id {adr_id} is used by {', '.join(files)}")
    constitution = read(CONSTITUTION)
    if INDEX_ROW.findall(constitution) != index_rows():
        problems.append(f"{CONSTITUTION}: ADR-009@v2 C10, C14: the index doesn't match the ADRs' front matter; "
                        "run scripts/adr.py index --write")
    for rule in hard_rules():
        if rule not in constitution.splitlines():
            problems.append(f"{CONSTITUTION}: ADR-009@v2 C17: hard rule not quoted word for word: {rule[:60]}…")
    for p in problems:
        print(p, file=sys.stderr)
    print(f"{len(adr_paths())} ADRs checked, {len(problems)} problems")
    return 1 if problems else 0


def write_index():
    text = read(CONSTITUTION)
    rows = INDEX_ROW.findall(text)
    if not rows:
        print("no index rows found to replace", file=sys.stderr)
        return 1
    start, end = text.index(rows[0]), text.index(rows[-1]) + len(rows[-1])
    with open(os.path.join(ROOT, CONSTITUTION), "w", encoding="utf-8", newline="\n") as f:
        f.write(text[:start] + "\n".join(index_rows()) + text[end:])
    return 0


def main(argv):
    # UTF-8 output on every system: Windows would otherwise use its code page, and the ADRs aren't ASCII
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if argv[:1] == ["check"]:
        return check(argv[argv.index("--base") + 1] if "--base" in argv else None)
    if argv[:1] == ["index"]:
        if "--write" in argv:
            return write_index()
        print("\n".join(index_rows()))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
