import { Plugin } from "@opencode/plugin"
import { expandDetails } from "./lib"

export default Plugin.define({
  id: "prompt-snippets",
  async setup(ctx) {
    await ctx.session.hook("prompt", async (event) => {
      if (!event.prompt.text) return
      const expansion = await expandDetails(event.prompt.text)
      event.prompt.text = expansion.text
      event.prompt.files = expansion.remapMentions(event.prompt.files)
      event.prompt.agents = expansion.remapMentions(event.prompt.agents)
      event.prompt.skills = expansion.remapMentions(event.prompt.skills)
    })
  },
})
