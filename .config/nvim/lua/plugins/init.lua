return {
    {
        "stevearc/conform.nvim",
        -- event = 'BufWritePre', -- uncomment for format on save
        opts = require "configs.conform",
    },

    -- These are some examples, uncomment them if you want to see them work!
    {
        "neovim/nvim-lspconfig",
        config = function()
            require "configs.lspconfig"
        end,
    },

{
    "hrsh7th/nvim-cmp",
    config = function(_, opts)
        local cmp = require("cmp")

        local custom_mapping = {
            ["<Up>"] = cmp.mapping.select_prev_item(),
            ["<Down>"] = cmp.mapping.select_next_item(),
            ["<Tab>"] = cmp.mapping.confirm({
                behavior = cmp.ConfirmBehavior.Replace,
                select = true,
            }),
            ["<CR>"] = cmp.config.disable,
        }

        opts.mapping = vim.tbl_deep_extend("force", opts.mapping, custom_mapping)
        cmp.setup(opts)
    end,
}

    -- test new blink
    -- { import = "nvchad.blink.lazyspec" },
    --
    -- {
    --     "nvim-treesitter/nvim-treesitter",
    --     opts = {
    --         ensure_installed = {
    --             "vim", "lua", "vimdoc",
    --             "html", "css"
    --         },
    --     },
    -- },
}
