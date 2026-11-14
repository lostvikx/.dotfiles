# Prompt Snippets

Mix-and-match single-purpose prompt rules that are inserted before, after, or
inline with your message when you send it. Each snippet is a tiny, standalone
instruction.

## Usage

- Press **alt+s** in the composer, or run **/snippet** (or **/snippets**), to
  open the snippet picker.
- The picker shows each snippet's display name and tag, for example
  `Ask questions (#ask-questions)`. Without a frontmatter `name`, only the tag
  is shown.
- Type to search, use `up`/`down` to navigate, `enter` to select, and `esc` to
  cancel.
- Selecting a snippet inserts its tag into the composer without sending the
  prompt:

  ```text
  #verify-not-assume 
  ```

- Press **alt+s** again to add another tag. Unlike slash commands, the keybind
  works mid-prompt. Slash commands are only recognized while the prompt is
  empty, so use **alt+s** to add tags while composing. Multiple tags are
  supported:

  ```text
  #verify-not-assume #ask-questions
  ```

- When you send the prompt, `prepend` snippets are added before your text,
  `append` snippets after it, and `inline` snippets replace their tag directly.
  Snippets within each group are sorted by `order`.
- A line containing only `prepend`/`append` tags is removed. Written next to
  text, a tag removes a following comma, semicolon, or colon and keeps
  sentence-ending punctuation.
- Expansion preserves your indentation and remaps `@file`, agent, and skill
  mention offsets so attachments still resolve.
- The picker re-scans `snippets/` every time it opens, and the server re-scans
  it on every prompt, so edits take effect immediately.

## Snippet files

Snippets live in `snippets/` next to `index.ts` — one Markdown file each, with
optional frontmatter:

```markdown
---
name: Concise
description: Keep answers short and to the point
placement: prepend
order: 10
---
Keep your response concise. Skip preamble and unnecessary explanation.
```

The filename without `.md` is the tag you insert. For example,
`verify-not-assume.md` becomes `#verify-not-assume`. Tags are case-insensitive;
`#foo` resolves to `Foo.md`.

| Field | Required | Notes |
|---|---|---|
| `name` | no | Display name; defaults to the filename without `.md` |
| `description` | no | Shown beside the snippet title in the picker; defaults to the first body line |
| `placement` | no | `prepend`, `append`, or `inline` (default: `inline`) |
| `order` | no | Number; sorts snippets within their group (default: `100`, ties broken by tag) |

## Development

Run the unit tests from this directory:

```sh
node --test lib.test.ts
```
