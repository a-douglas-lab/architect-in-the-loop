"""Translators: artefacts to glossary term IDs. Parameters are pre-registered in expected.md."""
import math
import re

from .artefacts import sentences
from .glossary import Glossary

STOPWORDS = frozenset("a an the of to in on off for and or by is it its as at be with".split())
K1, B, THRESHOLD = 1.5, 0.75, 1.5


def alias_pattern(alias: str) -> re.Pattern:
    return re.compile(r"(?<![\w/])" + re.escape(alias.lower()) + r"(?![\w/])")


def alias_hits(text: str, g: Glossary) -> set[str]:
    low = text.lower()
    return {t.id for t in g.terms.values() if any(alias_pattern(a).search(low) for a in t.aliases)}


def alias(arts: dict[str, str], g: Glossary) -> list[str]:
    return sorted(alias_hits("\n".join(arts.values()), g))


def stem(word: str) -> str:
    for suffix in ("ing", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def tokens(text: str) -> list[str]:
    return [stem(w) for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOPWORDS]


def bm25(arts: dict[str, str], g: Glossary) -> list[str]:
    docs = {t.id: tokens(" ".join((t.label,) + t.aliases)) for t in g.terms.values()}
    n = len(docs)
    avgdl = sum(len(d) for d in docs.values()) / n
    df: dict[str, int] = {}
    for d in docs.values():
        for w in set(d):
            df[w] = df.get(w, 0) + 1
    found = set()
    for _, sentence in sentences(arts):
        query = set(tokens(sentence))
        for tid, d in docs.items():
            score = 0.0
            for w in query:
                tf = d.count(w)
                if not tf:
                    continue
                idf = math.log((n - df[w] + 0.5) / (df[w] + 0.5) + 1)
                score += idf * tf * (K1 + 1) / (tf + K1 * (1 - B + B * len(d) / avgdl))
            if score >= THRESHOLD:
                found.add(tid)
    return sorted(found)


def validate_ids(ids, g: Glossary) -> list[str]:
    """The constrained model's output passes only if every ID is in the glossary."""
    unknown = [i for i in ids if i not in g.terms]
    if unknown:
        raise ValueError(f"not in the glossary: {unknown}")
    return sorted(set(ids))
