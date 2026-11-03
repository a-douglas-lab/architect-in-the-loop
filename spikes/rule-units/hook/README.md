# Live hook run

Tests L1 to L4 in [server-expected.md](../server-expected.md): a Claude Code session in which a `PreToolUse` hook on the Skill tool calls the rule-unit MCP server, and `analyze` runs on a neutral copy of f8. Nothing under `.claude/` is edited; the hook and the server come from files passed on the command line.

**Run on 2 Nov, headless,** by the author with Andy's key: L1 to L4 held in one unblind run, L2 by inference ([results.md](../results.md), raw files in [runs/live/](../runs/live/)). For an unattended run, pass `--setting-sources "user,project"`, not `user` alone: `user` alone drops the project's skills, so the Skill call fails and the hook never fires. Leaving out `local` keeps `.claude/settings.local.json`'s broad allow rules out of the session.

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

3. For the model translator, set your API key in this shell first. Without one, the server falls back to alias and the log says so. I haven't confirmed that Claude Code passes the shell's environment to a stdio server; if the log's fallback reason is about authentication with the key set, it doesn't. Don't put the key in this repository. (For the 2 Nov run, Andy kept it in a `.env` file outside the repository, read into the run's environment only.)

4. Start the session from the repository root (Spec Kit resolves relative feature paths under the git root, the server under `${cwd}`; they agree only there):

   ```powershell
   claude --settings "$env:TEMP\rule-units-live\settings.json" --mcp-config "$env:TEMP\rule-units-live\mcp.json"
   ```

   Approve the `rule-units` server if asked. Then send exactly:

   > Use the speckit-analyze skill on the current feature.

   Don't type `/speckit-analyze`: the hooks docs say typing `/skillname` bypasses `PreToolUse`, so the hook wouldn't fire.

5. Send back: the `analyze` report, and `$env:TEMP\rule-units-live\hook-log.jsonl`. If the session shows the hook's reminder (or doesn't), say so.

## What each file does

- `settings.json`: one `PreToolUse` hook, matcher `Skill`, type `mcp_tool`, calling `rule_units_hook` with `skill` from `${tool_input.skill}`, `project_dir` from `${cwd}` and `hook_event_name`. The field name `tool_input.skill` is an assumption: the hooks docs don't name it. If the log shows an empty `skill`, it is wrong.
- `mcp.json`: starts `python -m ruleunits.server` from the spike venv, with the feature folder, no-persist and the log path in its environment.
- `x02/`: f8's spec, plan and tasks with the "(test fixture)" label removed, under the same neutral name as in the spike's runs.
