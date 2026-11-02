# Live hook run

Tests L1 to L4 in [server-expected.md](../server-expected.md): a Claude Code session in which a `PreToolUse` hook on the Skill tool calls the rule-unit MCP server, and `analyze` runs on a neutral copy of f8. Nothing under `.claude/` is edited; the hook and the server come from files passed on the command line.

## Steps (PowerShell, from this worktree)

1. Write the files outside the repository:

   ```powershell
   cd spikes\rule-units
   .venv\Scripts\python -m ruleunits hook-files "$env:TEMP\rule-units-live"
   cd ..\..
   ```

2. Point Spec Kit at the neutral copy, read-only:

   ```powershell
   $env:SPECIFY_FEATURE_DIRECTORY = "$env:TEMP\rule-units-live\x02"; $env:SPECIFY_FEATURE_NO_PERSIST = "1"
   ```

3. For the model translator, set your API key in this shell first. Without one, the server falls back to alias and the log says so. I haven't confirmed that Claude Code passes the shell's environment to a stdio server; if the log's fallback reason is about authentication with the key set, it doesn't. The key never goes in a file.

4. Start the session from the repository root:

   ```powershell
   claude --settings "$env:TEMP\rule-units-live\settings.json" --mcp-config "$env:TEMP\rule-units-live\mcp.json"
   ```

   Approve the `rule-units` server if asked. Then send exactly:

   > Use the speckit-analyze skill on the current feature.

5. Send back: the `analyze` report, and `$env:TEMP\rule-units-live\hook-log.jsonl`. If the session shows the hook's reminder (or doesn't), say so.

## What each file does

- `settings.json`: one `PreToolUse` hook, matcher `Skill`, type `mcp_tool`, calling `rule_units_hook` with `skill` from `${tool_input.skill}`, `project_dir` from `${cwd}` and `hook_event_name`.
- `mcp.json`: starts `python -m ruleunits.server` from the spike venv, with the feature folder, no-persist and the log path in its environment.
- `x02/`: f8's spec, plan and tasks with the "(test fixture)" label removed, under the same neutral name as in the spike's runs.
