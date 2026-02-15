#!/bin/sh

# More info: https://man.archlinux.org/man/extra/rofi/rofi-dmenu.5.en

ACTION=$(echo "   Selection to Clipboard |   Selection to File |   Fullscreen to Clipboard |   Fullscreen to File " | rofi -no-show-icons -sep '|' -dmenu -p 'Action' -l 4 -i)

case "$ACTION" in
    "   Selection to Clipboard ")
        maim --noopengl -s | xclip -selection clipboard -t image/png
        ;;
    "   Selection to File ")
        maim --noopengl -s ~/Pictures/Screenshots/$(date +%Y-%m-%d_%H-%M-%S).png
        ;;
    "   Fullscreen to Clipboard ")
        sleep 1 && maim --noopengl | xclip -selection clipboard -t image/png
        ;;
    "   Fullscreen to File ")
        sleep 1 && maim --noopengl ~/Pictures/Screenshots/$(date +%Y-%m-%d_%H-%M-%S).png
        ;;
    *)
        exit 1
        ;;
esac
