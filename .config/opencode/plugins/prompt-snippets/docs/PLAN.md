# Prompt Snippets

## Goal

Expand `#tag` snippets server-side and provide a single-select TUI picker that
inserts snippet tags into the composer without submitting the prompt.

## Implementation

- `lib.ts` contains the shared snippet directory, parser, loader, expansion
  logic, mention remapping, and tag insertion helper.
- `index.ts` registers the V2 prompt hook. It expands tags and rewrites
  file/agent/skill mention offsets to match the changed text.
- `tui.ts` registers `/snippet` (alias `/snippets`) and `alt+s`. It re-scans
  snippets each time, shows the display name and tag, re-checks the focused
  prompt editor after the dialog, and inserts the tag without submitting.
- `snippets/` contains one Markdown file per snippet with optional
  frontmatter.

## Behavior

- Selecting a snippet inserts its tag, not its body. Expansion stays on the
  server.
- `prepend` bodies are added before the prompt, `append` bodies after it, and
  `inline` bodies replace their tag directly.
- Tags are case-insensitive and resolve to the actual filename.
- A line containing only prepend/append tags is removed. When such a tag sits
  next to text, a following comma, semicolon, or colon is removed;
  sentence-ending punctuation is kept.
- Expansion preserves the user's indentation and remaps mention offsets so
  file, agent, and skill attachments still resolve.
- Multiple tags are supported and sorted by `order` within each group.
- An empty snippets directory or an unfocused prompt shows a toast instead of
  opening an empty dialog.

## Verification

- `node --test lib.test.ts` from this directory.
- `opencode plugin list` shows the plugin.
- `/snippet`, `/snippets`, and `alt+s` insert without submitting.
- A prompt with an `@file` mention plus a prepend snippet keeps a valid mention
  offset.
