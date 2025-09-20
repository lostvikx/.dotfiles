require("nvchad.configs.lspconfig").defaults()

local servers = { "html", "cssls", "ruff", "denols", "bashls" }

-- read :h vim.lsp.config for changing options of lsp servers 
-- Refer: https://github.com/neovim/nvim-lspconfig/blob/master/doc/configs.md

vim.lsp.config('ruff', {
    init_options = {
        settings = {
            organizeImports = true,
            logLevel = "debug"
        }
    }
})

vim.lsp.enable(servers)
