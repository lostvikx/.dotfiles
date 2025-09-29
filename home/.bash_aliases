# Useful bash aliases created by Vikram S. Negi

# list files
alias la='ls -Alh'
alias ll='ls -lh'

# navigation
alias ..='cd ..'
alias cls='clear'
alias md='mkdir -p'

# display info
alias bat='batcat'
alias df='df -h'

# package management
alias update='sudo apt update && sudo apt upgrade -y'
alias autoclean='sudo apt autoremove && sudo apt clean && sudo apt autoclean'

# copy to clipboard (usage: cat file.txt | copy)
alias copy='xclip -selection clipboard'

# py venv
alias py-venv='python -m venv .venv'

# misc 
alias path='echo $PATH | tr ":" "\n"'
alias now='date -R'
alias reload='source ~/.bashrc'
alias wallpaper-path='gsettings get org.gnome.desktop.background picture-uri-dark'
alias battery-status="upower -i /org/freedesktop/UPower/devices/battery_BAT0"
alias weather-report='curl -s https://wttr.in/'

# youtube download
alias yt-play="mpv --profile=1080p --fs"
alias yt-video-download="yt-dlp --config-locations ~/.config/yt-dlp/yt-dlp-config.conf"
alias yt-music-download="yt-dlp --config-locations ~/.config/yt-dlp/music-config.conf"

# tools
#alias build-resume='pandoc -s -V geometry:"top=1cm, bottom=1cm, left=2cm, right=2cm" -V fontsize=10pt -V linestretch=0.85 -V linkcolor=blue -V header-includes="\usepackage{nopageno}" -o resume.pdf'
alias catppuccin='lutgen apply --palette catppuccin-mocha'
alias myip='curl https://checkip.amazonaws.com'

# safety mechanisms
# alias rm='rm -i' # I like to live on the edge!
alias cp='cp -i'
alias mv='mv -i'
alias trash='mv -t ~/.trash'

# Arch
alias mirrorlist-update='sudo reflector -c India -p https -n 5 --sort rate --thread 10 --save /etc/pacman.d/mirrorlist'
