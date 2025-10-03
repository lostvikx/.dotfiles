#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

HISTCONTROL=ignoreboth
HISTSIZE=2000
HISTFILESIZE=2000

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

if [ -f ~/.api_keys ]; then
    . ~/.api_keys
fi

[ $TERM = 'xterm-kitty' ] && alias ssh='kitty +kitten ssh'

export PYTHONDONTWRITEBYTECODE=1
export EDITOR='vim'

# Colors in terminal
case "$TERM" in
    xterm-color | *-256color | xterm-kitty) color_prompt=yes;;
esac

alias ls='ls --color=auto'
alias grep='grep --color=auto'

if [ "$color_prompt" = "yes" ]; then
    PS1='[\[\033[32m\]\u\[\033[37m\]@\[\033[31m\]\h \[\033[34m\]\W\[\033[0m\]] \n\$ '
else
    PS1='[\u@\h \W] \n\$ '
fi

#PS1='[\u@\h \W] \n\$ '

# Refer the Arch Wiki: https://wiki.archlinux.org/title/Kitty#Terminal_issues_with_SSH
[ $TERM = 'xterm-kitty' ] && alias ssh='kitty +kitten ssh'

# Password Store
export PASSWORD_STORE_CHARACTER_SET='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*'
export PASSWORD_STORE_GENERATED_LENGTH=20

# Script files
export PATH="$PATH:$HOME/programming/scripts"
export GTK_CSD=0

. "$HOME/.cargo/env"
