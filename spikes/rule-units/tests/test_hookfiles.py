"""The live-run files, and the hook as Claude Code would call it. Written after hookfiles.py."""
import asyncio
import json
import re

import pytest

pytest.importorskip("mcp")
from mcp import Client, StdioServerParameters  # noqa: E402

from ruleunits import hookfiles  # noqa: E402


def substitute(template: dict, hook_input: dict) -> dict:
    """Claude Code's ${path} substitution into an mcp_tool hook's string inputs, as documented."""
    def lookup(path):
        value = hook_input
        for part in path.split("."):
            value = value.get(part, "") if isinstance(value, dict) else ""
        return str(value)
    return {k: re.sub(r"\$\{([^}]+)\}", lambda m: lookup(m.group(1)), v) for k, v in template.items()}


def test_files_written_and_neutral(tmp_path):
    paths = hookfiles.write(tmp_path)
    for kind in ("spec", "plan", "tasks"):
        assert "(test fixture)" not in (paths["feature"] / f"{kind}.md").read_text(encoding="utf-8")
    hook = json.loads(paths["settings"].read_text(encoding="utf-8"))["hooks"]["PreToolUse"][0]
    assert hook["matcher"] == "Skill"
    assert hook["hooks"][0]["type"] == "mcp_tool"
    server = json.loads(paths["mcp"].read_text(encoding="utf-8"))["mcpServers"][hookfiles.SERVER]
    assert server["env"]["SPECIFY_FEATURE_DIRECTORY"] == str(paths["feature"])


def test_generated_config_end_to_end(tmp_path):
    """Start the server from the generated MCP config, outside the spike folder, and call it with
    the generated hook's input after substitution from a sample PreToolUse payload."""
    paths = hookfiles.write(tmp_path / "live")
    cfg = json.loads(paths["mcp"].read_text(encoding="utf-8"))["mcpServers"][hookfiles.SERVER]
    hook = json.loads(paths["settings"].read_text(encoding="utf-8"))["hooks"]["PreToolUse"][0]["hooks"][0]
    payload = {"hook_event_name": "PreToolUse", "cwd": str(tmp_path), "tool_name": "Skill",
               "tool_input": {"skill": "speckit-analyze"}}
    args = substitute(hook["input"], payload)
    env = dict(cfg["env"], RULEUNITS_TRANSLATOR="alias")
    params = StdioServerParameters(command=cfg["command"], args=cfg["args"], env=env, cwd=str(tmp_path))

    async def go():
        async with Client(params, mode="legacy") as client:
            return await client.call_tool(hook["tool"], args)

    result = asyncio.run(go())
    out = json.loads("".join(c.text for c in result.content if getattr(c, "type", "") == "text"))
    assert "ADR-016@v1 C10" in out["hookSpecificOutput"]["additionalContext"]
    logged = [json.loads(line) for line in paths["log"].read_text(encoding="utf-8").splitlines()]
    assert logged[-1]["skill"] == "speckit-analyze" and logged[-1]["returned_context"]
