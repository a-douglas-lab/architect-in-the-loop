# First Claude Code session: prompt

Paste everything below the line into a new Claude Code session opened in the new repository folder, after the starting documents have been copied in.

---

We're starting Phase 1 (Foundations) of this project. Read CLAUDE.md, then product.md, backlog.md, roadmap.md, architecture-sketch.md and development-outcomes.md before doing anything else.

Work through the steps below **one at a time**. At the end of each step, stop, show me what you propose or produced, and wait for my approval before moving on. Challenge my decisions where you see a problem; don't assume anything that backlog.md doesn't record as decided.

**Step 1. Check your understanding.** Summarise the project in five sentences. Then list anything in the documents that is contradictory, unclear or out of date, and any questions you need answered before Phase 1.

**Step 2. Repository structure.** Propose a folder structure covering: the documents already here (product.md stays at the root), Spec Kit's files, ADRs, the capability's source code, the Ordering exemplar work, and Claude Code configuration. Include how eShop is pulled in at commit `dc7ea49` without copying it (for example a git submodule or a fetch script), with options and a recommendation.

**Step 3. Spec Kit.** Check the current Spec Kit release and its documentation for using it with Claude Code before installing anything; don't rely on memory. Propose how to initialise it, and which presets or extensions to consider (T1 lists the open questions). Initialise it only after I approve.

**Step 4. ADR template (backlog T2, ADR-000).** Follow the research method at the top of backlog.md, as a commodity item: compare Nygard and MADR briefly, then propose our template. It needs front matter for ID, status, scope tags, precedence (G5), supersedes, enforcement links (Q1) and exceptions (G12), and fixed sections that a parser can extract (Context, Decision, Constraints, Consequences, Alternatives, Enforcement).

**Step 5. ADRs for decisions already made.** List the decisions recorded as decided in backlog.md that deserve an ADR, grouped and in a sensible order, for my approval. Then write them using the template, linking each back to its backlog item.

**Step 6. Constitution.** Draft the Spec Kit constitution: a small set of principles (start from the thesis and "How we work" in CLAUDE.md) plus an ADR index (ID, title, one-line decision, scope tags). Keep it small; ADR detail stays in the ADRs.

**Step 7. Claude Code setup (backlog D1).** Propose, then build after approval: skills for writing an ADR and running a research spike; an adversarial reviewer subagent; hooks that run build, format and tests after edits and block writes to protected paths. Explain how each supports a Spec Kit stage.

Keep a short session log in docs/sessions/ (date, what was decided, what changed) so the next session can pick up where this one stops.
