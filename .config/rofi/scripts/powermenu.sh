#!/bin/sh

# More info: https://man.archlinux.org/man/extra/rofi/rofi-dmenu.5.en

ACTION=$(echo "   Lock |   Reboot |   Shutdown |   Sleep " | rofi -no-show-icons -sep '|' -dmenu -p 'Action' -l 4 -i)

case "$ACTION" in
    "   Lock ")
        betterlockscreen --quiet --lock dimblur --off 30
        ;;
    "   Reboot ")
        reboot
        ;;
    "   Shutdown ")
        poweroff
        ;;
    "   Sleep ")
        systemctl suspend
        ;;
    *)
        exit 1
        ;;
esac
