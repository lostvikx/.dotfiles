#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

HISTCONTROL=ignoreboth
HISTSIZE=1000
HISTFILESIZE=1000

case "$TERM" in
    xterm-color | *-256color | xterm-kitty) color_prompt=yes;;
esac

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

if [ -f ~/.api_keys ]; then
    . ~/.api_keys
fi

[ $TERM = 'xterm-kitty' ] && alias ssh='kitty +kitten ssh'

export PYTHONDONTWRITEBYTECODE=1
export EDITOR='vim'

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '

# Refer the Arch Wiki: https://wiki.archlinux.org/title/Kitty#Terminal_issues_with_SSH
[ $TERM = 'xterm-kitty' ] && alias ssh='kitty +kitten ssh'

# Password Store
export PASSWORD_STORE_CHARACTER_SET='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*'
export PASSWORD_STORE_GENERATED_LENGTH=20
