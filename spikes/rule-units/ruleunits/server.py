"""The rule-unit MCP server, over stdio: python -m ruleunits.server, from spikes/rule-units/.

Meant to be called by a harness hook ("type": "mcp_tool") or an orchestrator, not chosen by a model.
Set RULEUNITS_LOG to a file path to log each hook call as one JSON line.
"""
import json
import os
import time
from pathlib import Path

from mcp.server.mcpserver import MCPServer

from . import join
from .units import build_index, load_all

server = MCPServer("rule-units", instructions="Rule units: selects the ADR constraints and hard rules that apply to a feature, and runs their deterministic checks.")


def log(entry: dict) -> None:
    path = os.environ.get("RULEUNITS_LOG")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")


@server.tool(structured_output=False)
def rule_units_hook(skill: str = "", project_dir: str = ".", hook_event_name: str = "PreToolUse") -> str:
    """Hook output JSON for a Claude Code mcp_tool hook on the Skill tool."""
    start = time.time()
    out, record = join.hook_result(skill, Path(project_dir), hook_event_name)
    log({"time": start, "tool": "rule_units_hook", "skill": skill, "project_dir": project_dir,
         "hook_event_name": hook_event_name, "seconds": round(time.time() - start, 2),
         "returned_context": out != "{}", "record": record})
    return out


@server.tool(structured_output=False)
def get_rules(feature_dir: str, stage: str = "analyze") -> str:
    """The record for one feature and stage: terms, selected units, findings and measurements."""
    return json.dumps(join.run(Path(feature_dir), stage)["record"])


@server.tool(structured_output=False)
def index() -> str:
    """Every unit's identity and applicability, without rule text or checks."""
    return json.dumps(build_index(load_all()))


if __name__ == "__main__":
    server.run("stdio")
