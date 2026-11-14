# Prompt Snippets — Code Review

Reviewed the untracked `.config/opencode/plugins/prompt-snippets/` directory. There
is no commit base, so the whole directory is the change. I checked the V2
server/TUI plugin docs and exercised `lib.ts` directly.

Status: review only. No fixes have been applied.

## Findings

### 1. Medium — Expanding snippets leaves mention offsets stale

`index.ts:7-9`, `lib.ts:113`

The prompt hook rewrites `event.prompt.text`, but never updates the
`mention.start` / `mention.end` offsets in `event.prompt.files`,
`event.prompt.agents`, or `event.prompt.skills`. Prepend snippets shift every
offset; inline tags before a mention shift later offsets. The V2 prompt-hook
docs explicitly require rewriting or removing mention offsets when text
changes.

Impact: prompts that use `@file`, agent, or skill mentions together with
snippets can have mention metadata pointing at the wrong text or out of range,
breaking highlighting and potentially attachment/skill resolution.

Minimal fix: after expansion, drop mentions whose slice no longer matches
`mention.text`, or remap each offset through the same text edits. Add a test
with a file mention plus a prepend snippet.

### 2. Medium — Picker can insert a tag that the server will not expand

`tui.ts:65`, `lib.ts:19`

`editor.insertText(\`#${selected} \`)` does not ensure a boundary before the
tag. If the cursor follows a word character, the result is e.g.
`Please#ask-questions `. The server regex uses `(?<![\w&/#])`, so it
deliberately ignores that tag and sends it literally.

Reproduced:

```text
expand("Please#ask-questions") -> "Please#ask-questions"
```

Impact: the advertised mid-prompt `alt+s` workflow silently fails when invoked
directly after a word.

Fix: inspect `editor.plainText.slice(0, editor.cursorOffset)` and insert a
leading space when the previous character is a word character, or always insert
` #tag ` and let the server trim.

### 3. Low — Expansion damages whitespace and leaves punctuation artifacts

`lib.ts:104-107`, `lib.ts:113`

Two issues in the same rewrite path:

- `out.trim()` strips leading indentation from the user's text. A prompt
  starting with an indented code block and an `#ask-questions` tag loses the
  indentation.
- Removing a placement tag consumes the whitespace before it but not
  punctuation after it. `"Use #verify-not-assume, then continue."` becomes
  `"Use, then continue."`.

Reproduced:

```text
"    const x = 1\n#ask-questions\n" -> "const x = 1\n\nAsk questions..."
"Use #verify-not-assume, then continue." -> "Use, then continue.\n\nDo not assume..."
```

Fix: remove standalone tag lines with a line-aware regex, avoid trimming the
user's text globally, and handle adjacent punctuation explicitly.

### 4. Low — Frontmatter `name` is parsed but never displayed; README says it is

`lib.ts:39-40`, `tui.ts:56-58`, `README.md:55`

The picker title is always `#${snippet.name}`, where `snippet.name` is the
filename stem. `snippet.title` comes from frontmatter `name`, but it is only
used as a description fallback — and `parse()` already fills `description` from
the first body line, so for any non-empty snippet the frontmatter name is
effectively dead. `PLAN.md:27` says the picker should show `#filename`, so the
README is the inconsistent part.

Fix: either show `${snippet.title} (#${snippet.name})` in the picker, or remove
the `name` row from the README and document that the filename is the display
identifier.

## Minor notes

- `lib.ts:18-19,75,88`: `FILE` and `TAG` are case-insensitive, but the
  known-name lookup and `${name}.md` read are exact. `Foo.MD` is listed by the
  picker but fails to expand on a case-sensitive filesystem; `#Foo` also will
  not resolve `foo.md`. Use a map from tag to actual filename.
- `tui.ts:32,62`: the editor is captured before two awaits and only checked for
  `isDestroyed` afterward. If the picker can outlive a session/focus change,
  re-resolve `context.renderer.currentFocusedEditor` and validate it before
  inserting.
- `tui.ts:14-15`: the prompt detection depends on the host conventions
  `traits.owner === "opencode"` and `traits.role === "prompt"`. That works on
  v2.2.2, but the TUI plugin docs say host renderables are not part of the
  plugin API, so this is the most likely upgrade breakage point.
- `PLAN.md` still says `index.ts` reads from the old `.pi` path and that there
  is no TUI entrypoint, which contradicts the implementation. Update or remove
  it before committing.
- No automated tests. The mention-offset, insertion-boundary, and whitespace
  cases are straightforward unit tests for `lib.ts`.
- `.config/opencode/package.json` still declares V1
  `@opencode-ai/plugin@1.14.22`; the new V2 imports resolve at runtime for
  local plugins, but local typechecking will not resolve them.

## Verification

- `opencode plugin list` reports `prompt-snippets local`.
- `loadSnippets()` returns all six snippets with the expected placements and
  order.
- Direct `expand()` tests confirmed the boundary, whitespace, punctuation, and
  case behavior above.
- TUI `alt+s` behavior was confirmed by the user; it was not re-tested
  interactively during this review.
- No files were modified during the review.
