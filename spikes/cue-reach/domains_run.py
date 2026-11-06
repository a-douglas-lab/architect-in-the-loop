"""Cases in domains-expected.md. Usage: python -I spikes/cue-reach/domains_run.py

Needs CUE v0.17.1 (CUE_BIN, or %TEMP%/aitl-cue/bin/cue.exe). Each case copies domains/ to a
temporary folder, applies exact text edits, and runs `cue vet -c ./...`. I1 is answered by
impact(), which reads the import lines; CUE's own commands are listed to see if one does it.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "domains")
CUE = os.environ.get("CUE_BIN") or os.path.join(tempfile.gettempdir(), "aitl-cue", "bin", "cue.exe")
MODULE = "aitl.example/domains/"

CANON, AUTH, DATA, WF = "canon/canon.cue", "policy/auth/auth.cue", "policy/data/data.cue", "capability/workflow/workflow.cue"
ORD, HOOK, PAY = "ordering/ordering.cue", "webhooks/webhooks.cue", "payments/payments.cue"
PROD = "samepkg/producer.cue"

# id: (edits [(file, old, new)], expected, files the output must name, files it must not name)
CASES = {
    "B0": ([], "pass", [], []),
    "D1": ([(ORD, "\tstatus: #OrderStatus\n}", "\tstatus: #OrderStatus\n\tnote?:  string\n}")], "pass", [], []),
    "D2": ([(ORD, 'status: "shipped"}', 'status: "refunded"}')], "fail", ["ordering.cue"], ["webhooks.cue", "payments.cue"]),
    "S1": ([(CANON, "\ttrackingNumber: string", "\ttrackingNumber: int")], "fail", ["canon.cue", "webhooks.cue"], []),
    "S2": ([(CANON, "\ttrackingNumber: string\n", ""), (ORD, ', trackingNumber: "TRK123"', "")],
           "fail", ["webhooks.cue"], []),
    "S3": ([(PROD, "\ttrackingNumber: string\n", "")], "pass", [], []),
    "S4": ([(CANON, "\ttrackingNumber: string", "\ttrackingNo: string"), (ORD, 'trackingNumber: "TRK123"', 'trackingNo: "TRK123"')],
           "fail", ["webhooks.cue"], []),
    "S5": ([(CANON, "\ttrackingNumber: string\n", "\ttrackingNumber: string\n\testimatedDelivery?: string\n")], "pass", [], []),
    "S6": ([(CANON, '#Carrier: "royal-mail" | "ups" | "DHL"', '#Carrier: "royal-mail" | "ups"'), (ORD, 'carrier: "DHL"', 'carrier: "ups"')],
           "fail", ["webhooks.cue"], []),
    "S7": ([(CANON, 'currency: "GBP" | "EUR" | "USD"', 'currency: "GBP" | "EUR"')], "fail", ["payments.cue"], []),
    "X1": ([(ORD, '\t{path: "/orders", method: "POST"',
             '\t{path: "/orders/export", method: "GET", auth: "none", roles: [], admin: false, mfa: false},\n\t{path: "/orders", method: "POST"')],
           "fail", ["auth.cue"], []),
    "X2": ([(PAY, 'roles: ["customer"]', "roles: []")], "fail", ["auth.cue"], []),
    "X3": ([(AUTH, "\tif auth == \"none\" {", "\tif admin {\n\t\t// Auth ADR C3: admin endpoints need MFA\n\t\tmfa: true\n\t}\n\tif auth == \"none\" {")],
           "fail", ["ordering.cue", "payments.cue"], []),
    "X4": ([(ORD, "\tschemaVersion: 1\n", "")], "fail", [], []),
    "X5": ([(DATA, "maxRetentionDays: 365", "maxRetentionDays: 90")], "fail", ["webhooks.cue"], []),
    "X6": ([(CANON, "\temail:      data.#PIIField", "\temail: {value: string}")], "fail", ["data.cue"], []),
    "W1": ([(ORD, ', compensation: "release-stock"', "")], "fail", ["workflow.cue"], []),
    "W2": ([(WF, "maxStepTimeoutHours: 24", "maxStepTimeoutHours: 1")], "fail", ["payments.cue"], []),
    "W3": ([(WF, "#Workflow: {\n\tname: string", "#Workflow: {\n\tname:  string\n\towner: string")],
           "fail", ["ordering", "payments"], []),
    "I2": ([(CANON, "// amount is in pounds", "// amount is in pence")], "pass", [], []),
    "I3": ([(DATA, "\t...\n}", "\tif financial {\n\t\t// Audit ADR C1: financial events are kept at least seven years\n\t\tretentionDays: >=2555\n\t}\n"
                           "\tif hasPII {\n\t\t// Privacy ADR C1: events holding PII are kept at most a year\n\t\tretentionDays: <=365\n\t}\n\t...\n}")],
           "fail", ["data.cue", "payments.cue"], []),
    "I4": ([(HOOK, "canon.#OrderShipped & {trackingNumber: string}", "canon.#OrderShipped & {trackingNumber: int}")],
           "fail", ["webhooks.cue"], []),
    # X6b (dated expectation after run 1): X6 left an unused import, a compile error, so this removes it too
    "X6b": ([(CANON, "\temail:      data.#PIIField", "\temail: {value: string}"),
             (CANON, 'import "aitl.example/domains/policy/data"\n', "")],
            "fail", ["canon.cue", "payments.cue"], ["data.cue"]),
}

# Exploratory cases, run after run 2 and NOT pre-registered (review run 3 asked for them to be
# reproducible): id -> (edits, cue vet arguments, package). Results go in domains-results.md.
AUDIT = "\tif financial {\n\t\tretentionDays: >=2555\n\t}\n"
PRIVACY = "\tif hasPII {\n\t\tretentionDays: <=365\n\t}\n"
NO_VALUE = (PAY, "\tretentionDays: 2555\n", "")
EXPLORATORY = {
    "X6c canon drops the PII wrapper, payments drops classification": (
        [(CANON, "\temail:      data.#PIIField", "\temail: {value: string}"),
         (CANON, 'import "aitl.example/domains/policy/data"\n', ""),
         (PAY, ', classification: "personal"', "")], ["-c"], None),
    "I3a audit rule only": ([(DATA, "\t...\n}", AUDIT + "\t...\n}")], ["-c"], "payments"),
    "I3p privacy rule only": ([(DATA, "\t...\n}", PRIVACY + "\t...\n}")], ["-c"], "payments"),
    "I3n both rules, no retention value": ([(DATA, "\t...\n}", AUDIT + PRIVACY + "\t...\n}"), NO_VALUE], ["-c=false"], "payments"),
    "I3na audit only, no retention value (control)": ([(DATA, "\t...\n}", AUDIT + "\t...\n}"), NO_VALUE], ["-c=false"], "payments"),
    "S1 module-wide with -E": ([(CANON, "\ttrackingNumber: string", "\ttrackingNumber: int")], ["-c", "-E"], "..."),
    "X3 module-wide with -E": ([(AUTH, "\tif auth == \"none\" {", "\tif admin {\n\t\tmfa: true\n\t}\n\tif auth == \"none\" {")],
                               ["-c", "-E"], "..."),
    "W2 module-wide with -E": ([(WF, "maxStepTimeoutHours: 24", "maxStepTimeoutHours: 1")], ["-c", "-E"], "..."),
}

PACKAGES = ["canon", "policy/auth", "policy/data", "capability/workflow", "ordering", "webhooks", "payments", "samepkg"]
# Per-package mode (dated expectation after run 1): the packages expected to fail when each is vetted alone.
# X6 is left out: its compile error was a fault in the case, replaced by X6b.
EXPECTED_FAILING = {
    "B0": set(), "D1": set(), "D2": {"ordering"}, "S1": {"ordering", "webhooks"}, "S2": {"webhooks"}, "S3": set(),
    "S4": {"webhooks"}, "S5": set(), "S6": {"webhooks"}, "S7": {"payments"}, "X1": {"ordering"}, "X2": {"payments"},
    "X3": {"ordering", "payments"}, "X4": {"ordering"}, "X5": {"webhooks"}, "W1": {"ordering"},
    "W2": {"ordering", "payments"}, "W3": {"ordering", "payments"}, "I2": set(), "I3": {"payments"}, "I4": {"webhooks"},
    "X6b": {"payments"},
}


def impact(root, changed_pkg):
    """Packages that import changed_pkg, directly or through others, read from import lines."""
    imports = {}
    for dirpath, _, files in os.walk(root):
        if "cue.mod" in dirpath:
            continue
        for f in files:
            if f.endswith(".cue"):
                pkg = os.path.relpath(dirpath, root).replace("\\", "/")
                text = open(os.path.join(dirpath, f), encoding="utf-8").read()
                imports.setdefault(pkg, set()).update(re.findall(r'"' + re.escape(MODULE) + r'([^"]+)"', text))
    hit, frontier = set(), {changed_pkg}
    while frontier:
        nxt = {p for p, deps in imports.items() if deps & frontier and p not in hit}
        hit |= nxt
        frontier = nxt
    return sorted(hit)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print(subprocess.run([CUE, "version"], capture_output=True, text=True).stdout.splitlines()[0])
    commands = subprocess.run([CUE, "help"], capture_output=True, text=True).stdout
    listed = re.findall(r"^\s{2}(\w[\w-]*)\s", commands.split("Available Commands:")[-1], re.M)
    print("cue commands:", ", ".join(listed))
    mismatches = 0
    for cid, (edits, want, names, not_names) in CASES.items():
        root = tempfile.mkdtemp()
        dst = os.path.join(root, "domains")
        shutil.copytree(SRC, dst)
        for rel, old, new in edits:
            path = os.path.join(dst, rel)
            text = open(path, encoding="utf-8").read()
            assert text.count(old) == 1, (cid, rel, old)
            open(path, "w", encoding="utf-8").write(text.replace(old, new))
        r = subprocess.run([CUE, "vet", "-c", "./..."], cwd=dst, capture_output=True, text=True, encoding="utf-8")
        out = (r.stderr + r.stdout).replace(dst, "")
        # Per-package mode: vet each package alone; the failing ones are the affected domains
        failing, per_pkg = set(), {}
        for pkg in PACKAGES:
            p = subprocess.run([CUE, "vet", "-c", "./" + pkg], cwd=dst, capture_output=True, text=True, encoding="utf-8")
            if p.returncode:
                failing.add(pkg)
                per_pkg[pkg] = (p.stderr + p.stdout).replace(dst, "")
        all_out = out + "".join(per_pkg.values())
        got = "pass" if r.returncode == 0 else "fail"
        missing = [n for n in names if n not in all_out]
        unexpected = [n for n in not_names if n in all_out]
        ok = got == want and not missing and not unexpected
        want_failing = EXPECTED_FAILING.get(cid)
        pkg_ok = want_failing is None or failing == want_failing
        mismatches += not (ok and pkg_ok)
        print(f"\n{cid}: {got}, expected {want}: {'match' if ok else 'MISMATCH'}"
              + (f" (not named: {missing})" if missing else "") + (f" (named, unexpectedly: {unexpected})" if unexpected else "")
              + f"; failing packages {sorted(failing)}"
              + ("" if want_failing is None else f", expected {sorted(want_failing)}: {'match' if pkg_ok else 'MISMATCH'}"))
        for pkg, text in per_pkg.items():
            print(f"    [{pkg}] " + " | ".join(text.strip().splitlines()[:3]))
        shutil.rmtree(root, ignore_errors=True)
    print("\nExploratory cases (not pre-registered):")
    for label, (edits, args, pkg) in EXPLORATORY.items():
        root = tempfile.mkdtemp()
        dst = os.path.join(root, "domains")
        shutil.copytree(SRC, dst)
        for rel, old, new in edits:
            path = os.path.join(dst, rel)
            text = open(path, encoding="utf-8").read()
            assert text.count(old) == 1, (label, rel, old)
            open(path, "w", encoding="utf-8").write(text.replace(old, new))
        targets = ["./" + pkg] if pkg else ["./" + p for p in PACKAGES]
        results = []
        for target in targets:
            r = subprocess.run([CUE, "vet", *args, target], cwd=dst, capture_output=True, text=True, encoding="utf-8")
            first = (r.stderr + r.stdout).replace(dst, "").strip().splitlines()[:1]
            results.append(f"{target} exit {r.returncode}" + (f" ({first[0]})" if first else ""))
        print(f"  {label}: " + "; ".join(results))
        shutil.rmtree(root, ignore_errors=True)
    print("\nI1: packages importing canon (impact script):", impact(SRC, "canon"))
    print("I1: packages importing capability/workflow:", impact(SRC, "capability/workflow"))
    print("I1: packages importing policy/data:", impact(SRC, "policy/data"))
    print("D1: packages importing ordering:", impact(SRC, "ordering"))
    print(f"\nmismatches: {mismatches} of {len(CASES)}")
    return mismatches


if __name__ == "__main__":
    sys.exit(main())
