# ~/.bashrc file created by Vikram S. Negi

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Bash shell options: history
shopt -s histappend
shopt -s cmdhist
shopt -s lithist

# Bash shell options: navigation
shopt -s autocd
shopt -s cdspell

# Bash shell options: terminal
shopt -s checkwinsize

# Bash history
HISTSIZE=5000
HISTFILESIZE=10000
HISTCONTROL=ignoreboth

[ -f ~/.env ] && . ~/.env
[ -f ~/.api_keys ] && . ~/.api_keys
[ -f ~/.bash_aliases ] && . ~/.bash_aliases

# Rust cargo
. "$HOME/.cargo/env"

# Colors in terminal
case "$TERM" in
    xterm-color | *-256color | xterm-kitty) color_prompt=yes;;
esac

# PS1

if [ "$color_prompt" = "yes" ]; then
    GREEN='\[\033[32m\]'
    WHITE='\[\033[37m\]'
    RED='\[\033[31m\]'
    BLUE='\[\033[34m\]'
    YELLOW='\[\033[33m\]'
    RESET='\[\033[0m\]'

    PS1="[${GREEN}\u${WHITE}@${RED}\h ${BLUE}\w${YELLOW} (\$?)${RESET}]\n\$ "
else
    PS1='[\u@\h \w] \n\$ '
fi

[ $TERM = 'xterm-kitty' ] && alias ssh='kitty +kitten ssh'

# Environment variables
export EDITOR='vim'

# Disable __pycache__
export PYTHONDONTWRITEBYTECODE=1

# Password store
export PASSWORD_STORE_CHARACTER_SET='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*'
export PASSWORD_STORE_GENERATED_LENGTH=20
export PASSWORD_STORE_CLIP_TIME=30

# Personal script files
export PATH="$PATH:$HOME/.local/bin"

# Colors of ls
export LS_COLORS="$(vivid generate catppuccin-mocha)"
