# Useful bash aliases created by Vikram S. Negi

# list files and directories
alias la="ls -Alh"
alias ll="ls -lh"

# navigation
alias ..="cd .."
alias cls='clear'
alias md='mkdir -p'

# display info
alias bat='batcat'
alias df='df -h'

# package management
alias update='sudo apt update && sudo apt upgrade -y'
alias install='sudo apt install'
alias remove='sudo apt remove'
alias search='apt search'
alias autoclean='sudo apt autoremove --purge && sudo apt clean'

# copy to clipboard (usage: cat file.txt | copy)
alias copy="xclip -selection clipboard"

# python venv
alias py-venv="python -m venv .venv"

# weather 
alias weather-report="curl -s https://wttr.in/"

# system status
alias battery-status="upower -i /org/freedesktop/UPower/devices/battery_BAT0"

# youtube
alias yt-play="mpv --profile=1080p --fs"
alias yt-video-download="yt-dlp --config-locations ~/.config/yt-dlp/yt-dlp-config.conf"
alias yt-music-download="yt-dlp --config-locations ~/.config/yt-dlp/music-config.conf"

# pandoc
alias build-resume='pandoc -s -V geometry:"top=1cm, bottom=1cm, left=2cm, right=2cm" -V fontsize=12pt -V linestretch=0.85 -V linkcolor=blue -V header-includes="\usepackage{nopageno}" -o resume.pdf resume.md'

# safety mechanisms
# alias rm='rm -i' # I like to live on the edge!
alias cp='cp -i'
alias mv='mv -i'
alias trash='mv -t ~/.trash'
