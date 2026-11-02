Run the real speckit-analyze skill (invoke it with the Skill tool) on the feature in {FEATURE}.

The skill's prerequisites script finds the feature folder from environment variables. Run it from the repository root, C:\Users\adoug\Architect-in-the-loop\.claude\worktrees\spike-rule-units-0fd90a, with SPECIFY_FEATURE_DIRECTORY set to {FEATURE} and SPECIFY_FEATURE_NO_PERSIST set to 1, for example in bash:
SPECIFY_FEATURE_DIRECTORY='{FEATURE}' SPECIFY_FEATURE_NO_PERSIST=1 python .specify/scripts/python/check_prerequisites.py --json --require-spec --require-tasks --include-tasks

Also read {RULES}: rules that apply to this feature, selected for it. Take them into account in the analysis.

Otherwise read only what the skill tells you to. Don't read tests/ or spikes/. Don't modify any file in the repository.

Write the full analysis report the skill produces, in Markdown, to {OUT}. At the end of that file, add a section "Files opened" listing every file you read.

Then reply with one line: the path you wrote, and the number of CRITICAL findings.
