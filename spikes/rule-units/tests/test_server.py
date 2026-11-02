"""The MCP server over stdio, as a real subprocess: behaviour fixed in server-expected.md before the code."""
import asyncio
import json
import sys

import pytest

mcp = pytest.importorskip("mcp")
from mcp import Client, StdioServerParameters  # noqa: E402

from ruleunits import SPIKE, artefacts, report  # noqa: E402

F8 = artefacts.fixture_path("f8")


def params(env=None):
    # RULEUNITS_TRANSLATOR=alias keeps the tests off the network.
    base = {"RULEUNITS_TRANSLATOR": "alias", "SPECIFY_FEATURE_DIRECTORY": str(F8), "SPECIFY_FEATURE_NO_PERSIST": "1"}
    return StdioServerParameters(command=sys.executable, args=["-m", "ruleunits.server"], cwd=str(SPIKE),
                                 env={**base, **(env or {})})


def text_of(result):
    return "".join(c.text for c in result.content if getattr(c, "type", "") == "text")


async def with_client(mode, fn):
    async with Client(params(), mode=mode) as client:
        return await fn(client)


def call(mode, fn):
    return asyncio.run(with_client(mode, fn))


def test_m1_tools_listed():
    async def fn(client):
        return sorted(t.name for t in (await client.list_tools()).tools)
    assert call("auto", fn) == ["get_rules", "index", "rule_units_hook"]


@pytest.mark.parametrize("mode", ["legacy", "auto"])
def test_m2_hook_tool_returns_hook_output(mode, tmp_path):
    async def fn(client):
        return await client.call_tool("rule_units_hook", {
            "skill": "speckit-analyze", "project_dir": str(tmp_path), "hook_event_name": "PreToolUse"})
    out = json.loads(text_of(call(mode, fn)))
    ctx = out["hookSpecificOutput"]["additionalContext"]
    assert out["hookSpecificOutput"]["hookEventName"] == "PreToolUse"
    assert "ADR-016@v1 C10" in ctx and "not SARIF" in ctx


def test_m3_get_rules_record():
    async def fn(client):
        return await client.call_tool("get_rules", {"feature_dir": str(F8), "stage": "analyze"})
    rec = json.loads(text_of(call("auto", fn)))
    report.validate(rec)
    assert [f["ruleId"] for f in rec["findings"]] == ["ADR-016@v1 C10"]


def test_m4_index():
    async def fn(client):
        return await client.call_tool("index", {})
    assert len(json.loads(text_of(call("auto", fn)))) == 7
