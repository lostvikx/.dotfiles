set number
set encoding=utf-8
set mouse=a
set lazyredraw

syntax enable
filetype plugin indent on

set tabstop=4
set expandtab
set shiftwidth=4
set softtabstop=4

set autoindent
set smartindent

set hlsearch
set termguicolors

nnoremap <CR> :nohlsearch<CR><CR>

" Install theme: git clone https://github.com/catppuccin/vim.git ~/.vim/pack/vendor/start/catppuccin
colorscheme catppuccin_mocha
