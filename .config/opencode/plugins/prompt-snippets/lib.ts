import { readFile, readdir } from "node:fs/promises"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

export type Placement = "append" | "prepend" | "inline"

export type Snippet = {
  name: string
  title: string
  description: string
  body: string
  placement: Placement
}

export type Mention = {
  start: number
  end: number
  text: string
}

export type Mentioned = {
  mention?: Mention
}

type TextEdit = {
  start: number
  end: number
  text: string
}

type TagMatch = {
  start: number
  end: number
  tag: string
  file: string
}

type SnippetFile = {
  tag: string
  file: string
}

export type Expansion = {
  text: string
  remapMentions: <T extends Mentioned>(items: readonly T[] | undefined) => T[] | undefined
}

export const DIR = join(dirname(fileURLToPath(import.meta.url)), "snippets")

const FILE = /^[a-z][\w-]*\.md$/i
const TAG = /(?<![\w&/#])#([a-z][\w-]*)/gi

export function parse(name: string, raw: string): Snippet {
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/)
  const meta: Record<string, string> = {}
  let body = raw
  if (m) {
    body = raw.slice(m[0].length)
    for (const line of m[1].split(/\r?\n/)) {
      const i = line.indexOf(":")
      if (i > 0) meta[line.slice(0, i).trim()] = line.slice(i + 1).trim()
    }
  }
  const placement: Placement = ["append", "prepend", "inline"].includes(meta.placement)
    ? (meta.placement as Placement)
    : "inline"
  const content = body.trim()
  return {
    name,
    title: meta.name?.trim() || name,
    description: meta.description?.trim() || content.split(/\r?\n/, 1)[0]?.trim() || "",
    body: content,
    placement,
  }
}

const byTag = (a: Snippet, b: Snippet) => a.name.localeCompare(b.name)

export const byTitle = (a: Snippet, b: Snippet) =>
  a.title.localeCompare(b.title, undefined, { sensitivity: "base" }) ||
  a.name.localeCompare(b.name)

export async function listSnippetFiles(dir = DIR): Promise<string[]> {
  try {
    const files = await readdir(dir)
    return files.filter((file) => FILE.test(file)).sort((a, b) => a.localeCompare(b))
  } catch {
    return []
  }
}

export async function loadSnippets(dir = DIR): Promise<Snippet[]> {
  const files = await listSnippetFiles(dir)
  const loaded = await Promise.all(
    files.map(async (file) => {
      try {
        return parse(file.slice(0, -3), await readFile(join(dir, file), "utf8"))
      } catch {
        return undefined
      }
    }),
  )
  return loaded.filter((s): s is Snippet => s !== undefined).sort(byTag)
}

function indexTags(files: readonly string[]): Map<string, SnippetFile> {
  const index = new Map<string, SnippetFile>()
  for (const file of files) {
    const tag = file.slice(0, -3)
    const key = tag.toLowerCase()
    if (!index.has(key)) index.set(key, { tag, file })
  }
  return index
}

function findTags(text: string, index: Map<string, SnippetFile>): TagMatch[] {
  const matches: TagMatch[] = []
  for (const match of text.matchAll(new RegExp(TAG.source, TAG.flags))) {
    const start = match.index
    const snippet = index.get(match[1].toLowerCase())
    if (start === undefined || !snippet) continue
    matches.push({ start, end: start + match[0].length, ...snippet })
  }
  return matches
}

function spacesBefore(text: string, index: number): number {
  let i = index
  while (i > 0 && (text[i - 1] === " " || text[i - 1] === "\t")) i--
  return i
}

function spacesAfter(text: string, index: number): number {
  let i = index
  while (i < text.length && (text[i] === " " || text[i] === "\t")) i++
  return i
}

function lineStartAt(text: string, index: number): number {
  return text.lastIndexOf("\n", index - 1) + 1
}

function lineRemoval(text: string, lineStart: number, lineEnd: number, newline: number): TextEdit {
  if (newline !== -1) return { start: lineStart, end: newline + 1, text: "" }
  const previous = text[lineStart - 1] === "\n" && text[lineStart - 2] === "\r"
    ? lineStart - 2
    : lineStart - 1
  return { start: lineStart > 0 ? previous : 0, end: lineEnd, text: "" }
}

function placementEdit(text: string, match: TagMatch): TextEdit {
  const { start, end } = match
  const lineStart = lineStartAt(text, start)
  const newline = text.indexOf("\n", end)
  const lineEnd = newline === -1 ? text.length : newline
  const before = text.slice(lineStart, start)
  const after = text.slice(end, lineEnd)

  // A tag alone on its line removes the whole line.
  if (!before.trim() && !after.trim()) return lineRemoval(text, lineStart, lineEnd, newline)

  const right = spacesAfter(text, end)
  const punct = text[right]

  // Remove clause punctuation that would otherwise be left behind.
  if (punct === "," || punct === ";" || punct === ":") {
    return { start, end: spacesAfter(text, right + 1), text: "" }
  }

  // Keep sentence terminators but remove the space before them. A tag at the
  // start of a line has no preceding sentence, so drop the punctuation too.
  if (punct === "." || punct === "!" || punct === "?") {
    if (!before.trim()) return { start, end: spacesAfter(text, right + 1), text: "" }
    return { start: spacesBefore(text, start), end: right, text: "" }
  }

  // Keep one separator when the tag sat between words.
  if (before.trim()) return { start: spacesBefore(text, start), end, text: "" }
  // Preserve a run of spaces after a line-start tag as indentation.
  if (right > end + 1) return { start, end, text: "" }
  return { start, end: right, text: "" }
}

// Remove whole lines that contain only prepend/append tags and whitespace,
// including when several tags share the line.
function placementLineEdits(text: string, matches: readonly TagMatch[]): Map<number, TextEdit> {
  const groups = new Map<number, TagMatch[]>()
  for (const match of matches) {
    const lineStart = lineStartAt(text, match.start)
    const group = groups.get(lineStart)
    if (group) group.push(match)
    else groups.set(lineStart, [match])
  }

  const edits = new Map<number, TextEdit>()
  for (const [lineStart, group] of groups) {
    const sorted = group.slice().sort((a, b) => a.start - b.start)
    const last = sorted[sorted.length - 1]
    const newline = text.indexOf("\n", last.end)
    const lineEnd = newline === -1 ? text.length : newline
    let cursor = lineStart
    let covered = true
    for (const match of sorted) {
      if (text.slice(cursor, match.start).trim()) {
        covered = false
        break
      }
      cursor = match.end
    }
    if (!covered || text.slice(cursor, lineEnd).trim()) continue
    edits.set(lineStart, lineRemoval(text, lineStart, lineEnd, newline))
  }
  return edits
}

function normalizeEdits(edits: TextEdit[]): TextEdit[] {
  const sorted = edits.slice().sort((a, b) => a.start - b.start || a.end - b.end)
  const out: TextEdit[] = []
  for (const edit of sorted) {
    const last = out[out.length - 1]
    if (last && edit.start < last.end) {
      if (!last.text && !edit.text) {
        last.end = Math.max(last.end, edit.end)
        continue
      }
      continue
    }
    out.push({ ...edit })
  }
  return out
}

function applyEdits(text: string, edits: readonly TextEdit[]): string {
  let out = ""
  let cursor = 0
  for (const edit of edits) {
    out += text.slice(cursor, edit.start) + edit.text
    cursor = edit.end
  }
  return out + text.slice(cursor)
}

function remapRange(mention: Mention, edits: readonly TextEdit[]): [number, number] | undefined {
  let delta = 0
  for (const edit of edits) {
    if (edit.end <= mention.start) {
      delta += edit.text.length - (edit.end - edit.start)
      continue
    }
    if (edit.start >= mention.end) break
    return undefined
  }
  return [mention.start + delta, mention.end + delta]
}

function remapItems<T extends Mentioned>(
  items: readonly T[] | undefined,
  text: string,
  edits: readonly TextEdit[],
): T[] | undefined {
  if (!items) return items
  const out: T[] = []
  for (const item of items) {
    if (!item.mention) {
      out.push(item)
      continue
    }
    const range = remapRange(item.mention, edits)
    if (!range) continue
    const [start, end] = range
    if (text.slice(start, end) !== item.mention.text) continue
    out.push({ ...item, mention: { ...item.mention, start, end } })
  }
  return out
}

const unchanged = <T extends Mentioned>(items: readonly T[] | undefined): T[] | undefined =>
  items ? [...items] : undefined

export async function expandDetails(text: string, dir = DIR): Promise<Expansion> {
  const files = await listSnippetFiles(dir)
  const index = indexTags(files)
  if (!index.size) return { text, remapMentions: unchanged }

  const matches = findTags(text, index)
  if (!matches.length) return { text, remapMentions: unchanged }

  const used = [...new Map(matches.map((match) => [match.tag, match.file])).entries()]
  const loaded = await Promise.all(
    used.map(async ([tag, file]) => {
      try {
        return parse(tag, await readFile(join(dir, file), "utf8"))
      } catch {
        return undefined
      }
    }),
  )
  const snippets = loaded.filter((s): s is Snippet => s !== undefined)
  if (!snippets.length) return { text, remapMentions: unchanged }

  const byName = new Map(snippets.map((snippet) => [snippet.name, snippet]))
  const placement = matches.filter((match) => {
    const snippet = byName.get(match.tag)
    return snippet !== undefined && snippet.placement !== "inline"
  })
  const lineEdits = placementLineEdits(text, placement)
  const tagEdits: TextEdit[] = [...lineEdits.values()]
  for (const match of matches) {
    const snippet = byName.get(match.tag)
    if (!snippet) continue
    if (snippet.placement === "inline") {
      tagEdits.push({ start: match.start, end: match.end, text: snippet.body })
      continue
    }
    if (lineEdits.has(lineStartAt(text, match.start))) continue
    tagEdits.push(placementEdit(text, match))
  }

  const edits = normalizeEdits(tagEdits)
  if (!edits.length) return { text, remapMentions: unchanged }

  const core = applyEdits(text, edits)
  const pre = snippets
    .filter((snippet) => snippet.placement === "prepend")
    .sort(byTag)
    .map((snippet) => snippet.body)
    .join("\n\n")
  const post = snippets
    .filter((snippet) => snippet.placement === "append")
    .sort(byTag)
    .map((snippet) => snippet.body)
    .join("\n\n")

  const hasCore = core.trim().length > 0
  const leadTrim = hasCore && pre ? (core.match(/^(?:[ \t]*\r?\n)+/)?.[0].length ?? 0) : 0
  let finalText = hasCore ? core.slice(leadTrim) : ""
  if (hasCore) {
    if (pre) finalText = `${pre}\n\n${finalText}`
    if (post) finalText = `${finalText.replace(/(?:\r?\n[ \t]*)+$/, "")}\n\n${post}`
  } else {
    finalText = [pre, post].filter(Boolean).join("\n\n")
  }

  const remapMentions = <T extends Mentioned>(items: readonly T[] | undefined): T[] | undefined => {
    let mapped = remapItems(items, core, edits)
    if (!mapped) return mapped

    if (leadTrim) {
      const shifted: T[] = []
      for (const item of mapped) {
        if (!item.mention) {
          shifted.push(item)
        } else if (item.mention.start >= leadTrim) {
          shifted.push({
            ...item,
            mention: {
              ...item.mention,
              start: item.mention.start - leadTrim,
              end: item.mention.end - leadTrim,
            },
          })
        }
      }
      mapped = shifted
    }

    if (pre) {
      const shift = pre.length + 2
      mapped = mapped.map((item) =>
        item.mention
          ? {
              ...item,
              mention: {
                ...item.mention,
                start: item.mention.start + shift,
                end: item.mention.end + shift,
              },
            }
          : item,
      )
    }

    return mapped.filter(
      (item) =>
        !item.mention ||
        finalText.slice(item.mention.start, item.mention.end) === item.mention.text,
    )
  }

  return { text: finalText, remapMentions }
}

export async function expand(text: string, dir = DIR): Promise<string> {
  return (await expandDetails(text, dir)).text
}

export function tagInsertion(text: string, cursor: number, name: string): string {
  const offset = Math.max(0, Math.min(cursor, text.length))
  const before = text.slice(0, offset)
  const after = text.slice(offset)
  const lead = /[\p{L}\p{N}\p{M}_&/#@]$/u.test(before) ? " " : ""
  const trail = !after || /^[\p{L}\p{N}\p{M}_&/#@-]/u.test(after) ? " " : ""
  return `${lead}#${name}${trail}`
}
