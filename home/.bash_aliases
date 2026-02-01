# Useful bash aliases created by Vikram S. Negi

# list files
alias la='ls -Alh'
alias ll='ls -lh'

# navigation
alias ..='cd ..'
alias cls='clear'
alias md='mkdir -p'

# display info
alias battery-status="upower -i /org/freedesktop/UPower/devices/battery_BAT0"

# copy to clipboard (usage: cat file.txt | copy)
alias copy-clipboard='xclip -selection clipboard >/dev/null 2>&1'

# py venv
alias py-venv='python -m venv .venv'

# misc
alias path='echo $PATH | tr ":" "\n"'
alias now='date -R'
alias reload='source ~/.bashrc'
alias weather-report='curl -s https://wttr.in/'

# youtube download
alias yt-play="mpv --profile=1080p --fs"
alias yt-video-download="yt-dlp --config-locations ~/.config/yt-dlp/yt-dlp-config.conf"
alias yt-music-download="yt-dlp --config-locations ~/.config/yt-dlp/music-config.conf"

# tools
alias catppuccin='lutgen apply --palette catppuccin-mocha'
alias myip='curl https://checkip.amazonaws.com'

# safety mechanisms
alias rm='rm -I'
alias cp='cp -i'
alias mv='mv -i'
alias trash='mv -t ~/.trash'

# pacman mirrorlist
alias update-mirrors='sudo reflector $(< ~/.config/reflector/reflector.conf)'

# HDMI Duplicate Display
alias duplicate-display='xrandr --output eDP-1 --mode 1920x1080 --output HDMI-1 --mode 1920x1080 --same-as eDP-1 --scale-from 1920x1080'
