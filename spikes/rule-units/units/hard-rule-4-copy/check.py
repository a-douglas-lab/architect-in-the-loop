"""CLAUDE.md hard rule 4, copy clause: never copy eShop files into this repo."""
import hashlib
import re

from ruleunits.artefacts import sentences
from ruleunits.report import Finding, location
from ruleunits.translate import alias_hits

NEGATION = re.compile(r"\b(not|no|nothing|never|don't|doesn't|mustn't)\b", re.IGNORECASE)


def check_artefacts(arts, glossary, citation):
    findings = []
    for kind, s in sentences(arts):
        hits = alias_hits(s, glossary)
        if {"file-copy", "subject-system"} <= hits and not NEGATION.search(s):
            findings.append(Finding(citation, f"Copies subject files into this repository: {s!r}",
                                    locations=[location(f"{kind}.md", s)]))
    return findings, {"sentences_flagged": len(findings)}


def _digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_tree(repo, subject, citation):
    subject_hashes = {_digest(p): p for p in subject.rglob("*") if p.is_file()}
    findings = []
    for p in sorted(repo.rglob("*")):
        if p.is_file() and "subject" not in p.relative_to(repo).parts[:1]:
            src = subject_hashes.get(_digest(p))
            if src:
                rel = p.relative_to(repo).as_posix()
                findings.append(Finding(citation, f"{rel} is identical to subject file {src.relative_to(subject).as_posix()}",
                                        locations=[location(rel)]))
    return findings, {"files_compared": sum(1 for p in repo.rglob('*') if p.is_file())}
