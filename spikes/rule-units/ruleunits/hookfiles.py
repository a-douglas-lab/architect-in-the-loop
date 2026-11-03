"""Files for the live hook run: a neutral feature copy, a settings file and an MCP config.

Written outside .claude/, so no protected path changes. Passed to Claude Code with
--settings and --mcp-config (hook/README.md).
"""
import json
import re
import sys
from pathlib import Path

from . import SPIKE
from .artefacts import load_fixture

SERVER = "rule-units"


def settings() -> dict:
    return {"hooks": {"PreToolUse": [{"matcher": "Skill", "hooks": [{
        "type": "mcp_tool",
        "server": SERVER,
        "tool": "rule_units_hook",
        "input": {"skill": "${tool_input.skill}", "project_dir": "${cwd}", "hook_event_name": "${hook_event_name}"},
    }]}]}}


def mcp_config(feature: Path, log: Path) -> dict:
    return {"mcpServers": {SERVER: {
        "type": "stdio",
        "command": sys.executable,
        "args": ["-m", "ruleunits.server"],
        "env": {
            "PYTHONPATH": str(SPIKE),
            "SPECIFY_FEATURE_DIRECTORY": str(feature),
            "SPECIFY_FEATURE_NO_PERSIST": "1",
            "RULEUNITS_LOG": str(log),
        },
    }}}


def write(out: Path, fixture: str = "f8", neutral_name: str = "x02") -> dict[str, Path]:
    out = out.resolve()
    feature = out / neutral_name
    feature.mkdir(parents=True, exist_ok=True)
    for kind, text in load_fixture(fixture).items():
        (feature / f"{kind}.md").write_text(re.sub(r"\s*\(test fixture\)", "", text), encoding="utf-8", newline="\n")
    log = out / "hook-log.jsonl"
    paths = {"feature": feature, "settings": out / "settings.json", "mcp": out / "mcp.json", "log": log}
    paths["settings"].write_text(json.dumps(settings(), indent=2) + "\n", encoding="utf-8", newline="\n")
    paths["mcp"].write_text(json.dumps(mcp_config(feature, log), indent=2) + "\n", encoding="utf-8", newline="\n")
    return paths
