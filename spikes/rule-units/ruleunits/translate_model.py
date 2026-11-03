"""The constrained model translator, called through the Anthropic API.

The same instructions as runs/prompts/translator.md, for one feature. Output is limited to the
glossary's IDs by a JSON schema, then checked again by validate_ids.
"""
import json

from .glossary import Glossary
from .translate import validate_ids

MODEL = "claude-opus-5-5"

INSTRUCTIONS = """You are translating feature documents into a fixed vocabulary.

Each glossary term has an id, a label, a definition and aliases. The aliases are examples of wording, not a complete list.

List the glossary term ids whose concept the documents refer to. Count a concept whether it is asserted or negated (for example "nothing is copied" still refers to copying), and whatever words are used for it. Use only ids that exist in the glossary. Return an empty list if none applies."""


class TranslatorFailed(Exception):
    """The model translator gave no usable answer; the caller falls back to alias."""


def glossary_text(g: Glossary) -> str:
    return "\n".join(
        f"- id: {t.id}\n  label: {t.label}\n  definition: {t.definition}\n  aliases: {', '.join(t.aliases)}"
        for t in g.terms.values()
    )


def documents_text(arts: dict[str, str]) -> str:
    return "\n\n".join(f'<document name="{k}.md">\n{v}\n</document>' for k, v in arts.items())


def schema(g: Glossary) -> dict:
    return {
        "type": "object",
        "properties": {"terms": {"type": "array", "items": {"type": "string", "enum": g.ids()}}},
        "required": ["terms"],
        "additionalProperties": False,
    }


def default_client():
    import anthropic
    return anthropic.Anthropic()


def model(arts: dict[str, str], g: Glossary, client=None) -> list[str]:
    try:
        client = client or default_client()
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            output_config={"effort": "medium", "format": {"type": "json_schema", "schema": schema(g)}},
            system=INSTRUCTIONS,
            messages=[{"role": "user", "content": f"<glossary>\n{glossary_text(g)}\n</glossary>\n\n{documents_text(arts)}"}],
        )
    except Exception as e:  # any API, network or credential failure
        raise TranslatorFailed(f"model call failed: {type(e).__name__}: {e}") from e
    if response.stop_reason == "refusal":
        raise TranslatorFailed("model call ended in refusal")
    if response.stop_reason == "max_tokens":
        raise TranslatorFailed("model output cut off at max_tokens")
    text = next((b.text for b in response.content if b.type == "text"), "")
    try:
        ids = json.loads(text)["terms"]
    except (ValueError, KeyError, TypeError) as e:
        raise TranslatorFailed(f"model output not the expected JSON: {e}") from e
    try:
        return validate_ids(ids, g)
    except ValueError as e:
        raise TranslatorFailed(f"validator rejected the output: {e}") from e
