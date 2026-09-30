# Project Context & Agent Directives

## Core Rules

* Keep responses concise and actionable; avoid unnecessary explanation.
* Prefer small, incremental diffs over large changes.
* Do not assume architecture, patterns, dependencies, or features. Ask when requirements are unclear.
* Use `context7` for documentation lookup.
* Use `gh_grep` to find relevant GitHub implementations when unsure how something should be done.

## Planning

* Clarify ambiguous requirements, scope, or feature behavior before planning.
* Use read-only background agents (e.g. `@scout`, `@explore`) to investigate the codebase, dependencies, and existing patterns.
* Review and validate the plan with background agents before presenting it.
* Keep planning proportional to the task; avoid unnecessary planning for trivial changes.

## Implementation

* Prefer existing project patterns and utilities over introducing new abstractions.
* Delegate complex implementation work to specialized sub-agents when appropriate.
* Keep the primary agent focused by offloading research, exploration, and other context-heavy work to read-only sub-agents.
* Make the smallest change that fully solves the task.
* Verify changes with appropriate tests, checks, or builds before considering the task complete.
