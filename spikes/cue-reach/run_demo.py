"""Cases Q1 to Q8 in demo-expected.md. Usage: python -I spikes/cue-reach/run_demo.py

Needs CUE v0.17.1: set CUE_BIN, or unpack it to %TEMP%/aitl-cue/bin/cue.exe. Each case copies
model/ and data/ to a temporary folder, makes its change there, and runs `cue vet -c`.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CUE = os.environ.get("CUE_BIN") or os.path.join(tempfile.gettempdir(), "aitl-cue", "bin", "cue.exe")


def change_data(pattern, repl):
    def go(root):
        path = os.path.join(root, "data", "dev1.yaml")
        text = open(path, encoding="utf-8").read()
        new = re.sub(pattern, repl, text, count=1, flags=re.M)
        assert new != text, pattern
        open(path, "w", encoding="utf-8").write(new)
    return go


def add_model(text):
    def go(root):
        open(os.path.join(root, "model", "adr099.cue"), "w", encoding="utf-8").write(text)
    return go


CONFLICT = 'package aitl\n\n// A test clause that clashes with ADR-017@v1 C5\n#OutcomeRequest: stated_by: "merchant"\n'
COMPATIBLE = 'package aitl\n\n// A test clause that is compatible with ADR-017@v1 C5\n#OutcomeRequest: stated_by: string\n'

CASES = [  # id, change, use data?, expected exit (0 pass, nonzero fail)
    ("Q1", None, True, "pass"),
    ("Q2", change_data(r"^  areas_touched: \[(.*)\]$", r"  areas_touched: [\1, basket]"), True, "fail"),
    ("Q3", change_data(r"^  id: DEV-1$", "  id: EVAL-3"), True, "fail"),
    ("Q4", change_data(r"^    hidden: \[.*\]$", "    hidden: []"), True, "fail"),
    ("Q5", change_data(r'"ADR-005@v3 C6"', '"ADR-005 C6"'), True, "fail"),
    ("Q6", add_model(CONFLICT), True, "fail"),
    ("Q7", add_model(COMPATIBLE), True, "pass"),
    ("Q8", add_model(CONFLICT), False, "fail"),
]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print(subprocess.run([CUE, "version"], capture_output=True, text=True).stdout.splitlines()[0])
    fails = 0
    for cid, change, use_data, want in CASES:
        root = tempfile.mkdtemp()
        shutil.copytree(os.path.join(HERE, "model"), os.path.join(root, "model"))
        shutil.copytree(os.path.join(HERE, "data"), os.path.join(root, "data"))
        if change:
            change(root)
        cmd = [CUE, "vet", "-c", "./model"] + (["data/dev1.yaml"] if use_data else [])
        start = time.perf_counter()
        r = subprocess.run(cmd, cwd=root, capture_output=True, text=True, encoding="utf-8")
        took = time.perf_counter() - start
        got = "pass" if r.returncode == 0 else "fail"
        ok = got == want
        fails += not ok
        print(f"\n{cid}: exit {r.returncode} ({got}), expected {want}: {'match' if ok else 'MISMATCH'}; {took:.2f}s")
        for line in (r.stderr or r.stdout).strip().splitlines()[:8]:
            print("    " + line.replace(root, "<tmp>"))
        shutil.rmtree(root, ignore_errors=True)
    print(f"\nmismatches: {fails}")
    return fails


if __name__ == "__main__":
    sys.exit(main())
