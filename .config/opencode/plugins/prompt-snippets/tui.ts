import { Plugin } from "@opencode/plugin/tui"
import type { EditBufferRenderable } from "@opentui/core"
import { DIR, byTitle, loadSnippets, tagInsertion } from "./lib"

type PromptTraits = {
  owner?: string
  role?: string
}

function isPromptEditor(
  editor: EditBufferRenderable | null,
): editor is EditBufferRenderable {
  if (!editor || editor.isDestroyed) return false
  const traits = editor.traits as unknown as PromptTraits
  return traits.owner === "opencode" && traits.role === "prompt"
}

export default Plugin.define({
  id: "prompt-snippets.tui",
  setup(context) {
    context.keymap.layer(() => ({
      mode: "global",
      commands: [
        {
          id: "prompt-snippets.insert",
          title: "Insert prompt snippet",
          description: "Insert a snippet tag into the prompt",
          group: "Prompt Snippets",
          bind: "alt+s",
          slash: { name: "snippet", aliases: ["snippets"] },
          run: async () => {
            const editor = context.renderer.currentFocusedEditor
            if (!isPromptEditor(editor)) {
              context.ui.toast.show({
                title: "Prompt snippets",
                message: "Focus the prompt, then press alt+s or run /snippet.",
                variant: "warning",
              })
              return
            }

            const snippets = await loadSnippets()
            if (!snippets.length) {
              context.ui.toast.show({
                title: "Prompt snippets",
                message: `No snippets found in ${DIR}`,
                variant: "warning",
              })
              return
            }

            const selected = await context.ui.dialog.select({
              title: "Insert prompt snippet",
              placeholder: "Search snippets...",
              options: snippets.slice().sort(byTitle).map((snippet) => ({
                title: snippet.title,
                value: snippet.name,
                footer: snippet.placement,
              })),
            })
            if (!selected) return

            // Focus is restored asynchronously after the dialog closes, so prefer
            // the live editor but fall back to the one captured before opening it.
            const current = context.renderer.currentFocusedEditor
            const target = isPromptEditor(current) ? current : isPromptEditor(editor) ? editor : undefined
            if (!target) return

            target.focus()
            target.insertText(tagInsertion(target.plainText, target.cursorOffset, selected))
          },
        },
      ],
    }))
  },
})
