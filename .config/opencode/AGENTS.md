# Global Agent Directives

## Core

- Be concise and actionable; omit filler.
- Make the smallest change that fully solves the task; prefer incremental diffs.
- Match existing patterns, style, and utilities. Avoid new abstractions or dependencies without a clear reason.
- Do not assume architecture, behavior, or conventions. Inspect the code first; ask when requirements are unclear.
- Preserve unrelated and uncommitted work. Investigate unfamiliar files before changing or deleting them.

## Planning

- Clarify scope, behavior, and constraints before planning non-trivial work.
- Investigate first: search the codebase, read relevant files, and check dependencies and configuration.
- Use read-only subagents (e.g. `explore`) for context-heavy research; keep the main context focused.
- Scale planning to the task. For non-trivial changes, share a short plan and assumptions before editing.

## Implementation

- Delegate complex or parallelizable work to specialized subagents when it helps.
- Keep edits scoped; avoid drive-by refactors and unrelated formatting changes.
- Do not add dependencies, generated files, or documentation unless asked or clearly required.

## Subagents

- Delegate when a task benefits from isolated context, parallel execution, or a specialist role. Handle small, single-file edits in the main agent.
- Route by strength: `explore` for read-only codebase and web research, `general` for multi-step work in parallel, `data-scientist` for dataset inspection and statistical analysis, `docs-writer` for READMEs, API docs, docstrings, and changelogs, `code-reviewer` for a second-pass diff review.
- Respect each agent's access: `code-reviewer` cannot use the edit/write/patch tools; `docs-writer` cannot run commands; `data-scientist` can write analysis artifacts but not modify application source. None of them can spawn further subagents.
- Pass the context each subagent needs in its prompt. It starts with a fresh context and never sees the parent conversation.
- Subagents always run in the background. Continue with non-overlapping work and do not poll for results.
- Do not delegate work that is faster to do directly, and never launch two subagents that would edit the same files.

## Verification

- Run the narrowest relevant checks (tests, typecheck, lint, build) and fix failures caused by your change.
- Do not fix unrelated failures; report them.
- If the project has no checks, validate syntax/config with the appropriate parser and state what could not be verified.
- Use the `code-reviewer` subagent for a second pass on non-trivial diffs when useful.
- Never claim success without evidence. In the final response, summarize what changed, where, and how it was verified.

## Safety

- Never commit, push, create branches, or rewrite history unless explicitly asked.
- Never run destructive commands. Ask before deleting files or taking other irreversible/high-impact actions.
- Never print, commit, or expose secrets (API keys, tokens, `.env` contents). Use environment variables.

## Tooling

- Use `context7` for current library and framework documentation.
- Use `gh_grep` for real-world implementation examples when local patterns are insufficient.
- Prefer repository evidence over memory; use web search for current information.

## GitHub

- Use `gh` for PR, issue, review, and Actions context: `gh pr list/view/diff`, `gh issue list/view`, `gh run list/view`.
- Read-only queries are fine. Ask before mutations: creating, editing, commenting on, closing, or merging PRs/issues, or pushing branches.
- Never merge or close a PR/issue without explicit confirmation.
- Prefer repository templates and `--body-file` for longer PR/issue bodies; link related issues.
- Never echo tokens or credentials from `gh auth status`.
