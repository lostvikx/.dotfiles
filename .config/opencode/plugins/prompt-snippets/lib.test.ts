import assert from "node:assert/strict"
import { mkdtemp, rm, writeFile } from "node:fs/promises"
import { tmpdir } from "node:os"
import { join } from "node:path"
import { after, before, test } from "node:test"
import { expand, expandDetails, loadSnippets, tagInsertion } from "./lib.ts"

let dir = ""

before(async () => {
  dir = await mkdtemp(join(tmpdir(), "prompt-snippets-"))
  await Promise.all([
    writeFile(
      join(dir, "pre-first.md"),
      "---\nname: First prepend\nplacement: prepend\norder: 10\n---\nPRE1",
    ),
    writeFile(
      join(dir, "pre.md"),
      "---\nname: Prepend\nplacement: prepend\norder: 20\n---\nPRE2",
    ),
    writeFile(
      join(dir, "post-first.md"),
      "---\nname: First append\nplacement: append\norder: 10\n---\nPOST1",
    ),
    writeFile(
      join(dir, "post.md"),
      "---\nname: Append\nplacement: append\norder: 20\n---\nPOST2",
    ),
    writeFile(join(dir, "inline.md"), "---\nplacement: inline\n---\nINLINE"),
    writeFile(join(dir, "Foo.MD"), "---\nname: Foo Case\nplacement: inline\n---\nCASE"),
  ])
})

after(async () => {
  await rm(dir, { recursive: true, force: true })
})

test("loads snippets from the provided directory", async () => {
  const snippets = await loadSnippets(dir)
  assert.equal(snippets.length, 6)
  assert.equal(snippets.find((snippet) => snippet.name === "Foo")?.title, "Foo Case")
})

test("does not expand a tag after a word character", async () => {
  assert.equal(await expand("Please#inline", dir), "Please#inline")
})

test("replaces inline tags", async () => {
  assert.equal(await expand("#inline and #inline", dir), "INLINE and INLINE")
})

test("orders prepend and append bodies", async () => {
  assert.equal(
    await expand("#pre-first\n#pre\nmiddle\n#post-first\n#post", dir),
    "PRE1\n\nPRE2\n\nmiddle\n\nPOST1\n\nPOST2",
  )
})

test("removes clause punctuation after a placement tag", async () => {
  assert.equal(
    await expand("Use #post, then continue.", dir),
    "Use then continue.\n\nPOST2",
  )
})

test("keeps sentence punctuation after a placement tag", async () => {
  assert.equal(
    await expand("Use #post. Then continue.", dir),
    "Use. Then continue.\n\nPOST2",
  )
})

test("preserves indentation while removing a standalone tag line", async () => {
  assert.equal(
    await expand("    const x = 1\n#post\n", dir),
    "    const x = 1\n\nPOST2",
  )
})

test("removes a standalone tag line between text lines", async () => {
  assert.equal(await expand("before\n#post\nafter", dir), "before\nafter\n\nPOST2")
})

test("removes a line containing several placement tags", async () => {
  assert.equal(
    await expand("#pre #post\nmiddle", dir),
    "PRE2\n\nmiddle\n\nPOST2",
  )
  assert.equal(
    await expand("before\n#pre #post\nafter", dir),
    "PRE2\n\nbefore\nafter\n\nPOST2",
  )
})

test("handles punctuation after a line-start placement tag", async () => {
  assert.equal(await expand("#post. Then continue.", dir), "Then continue.\n\nPOST2")
})

test("preserves indentation after a line-start placement tag", async () => {
  assert.equal(await expand("#post    const x = 1", dir), "    const x = 1\n\nPOST2")
  assert.equal(await expand("#post text", dir), "text\n\nPOST2")
})

test("resolves tags case-insensitively to the actual filename", async () => {
  assert.equal(await expand("#foo", dir), "CASE")
  assert.equal(await expand("#FOO", dir), "CASE")
})

test("remaps file, agent, and skill mentions through expansion", async () => {
  const text = "#pre\n@agent @file.ts @skill"
  const mention = (value: string) => ({
    start: text.indexOf(value),
    end: text.indexOf(value) + value.length,
    text: value,
  })
  const expansion = await expandDetails(text, dir)
  assert.equal(expansion.text, "PRE2\n\n@agent @file.ts @skill")

  const files = expansion.remapMentions([
    { uri: "file:///file.ts", mention: mention("@file.ts") },
  ])
  const agents = expansion.remapMentions([{ name: "agent", mention: mention("@agent") }])
  const skills = expansion.remapMentions([{ id: "skill", mention: mention("@skill") }])

  for (const [items, value] of [
    [files, "@file.ts"],
    [agents, "@agent"],
    [skills, "@skill"],
  ] as const) {
    const found = items?.[0]?.mention
    assert.equal(found?.start, expansion.text.indexOf(value))
    assert.equal(expansion.text.slice(found?.start, found?.end), value)
  }
})

test("remaps mentions after an inline tag", async () => {
  const text = "#inline @file.ts"
  const start = text.indexOf("@file.ts")
  const expansion = await expandDetails(text, dir)
  assert.equal(expansion.text, "INLINE @file.ts")

  const files = expansion.remapMentions([
    { mention: { start, end: start + "@file.ts".length, text: "@file.ts" } },
  ])
  assert.equal(files?.[0]?.mention?.start, "INLINE ".length)
  assert.equal(files?.[0]?.mention?.end, "INLINE @file.ts".length)
})

test("inserts a tag with safe spacing", async () => {
  assert.equal(tagInsertion("Please", 6, "inline"), " #inline ")
  assert.equal(tagInsertion("Please ", 7, "inline"), "#inline ")
  assert.equal(tagInsertion("a ", 1, "inline"), " #inline")
  assert.equal(tagInsertion("a", 1, "inline"), " #inline ")
  assert.equal(tagInsertion("", 0, "inline"), "#inline ")
})

test("keeps tags separate from mentions and non-ASCII words", async () => {
  assert.equal(tagInsertion("Please @file.ts", 7, "inline"), "#inline ")
  assert.equal(tagInsertion("café", 4, "inline"), " #inline ")
})
