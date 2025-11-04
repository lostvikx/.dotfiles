#!/bin/sh

# More info: https://man.archlinux.org/man/extra/rofi/rofi-dmenu.5.en

ACTION=$(echo "Hibernate,Lock,Reboot,Shutdown,Sleep" | rofi -no-show-icons -sep ',' -dmenu -p 'Action' -l 5 -i)

case "$ACTION" in
    "Hibernate")
        systemctl hibernate
        ;;
    "Lock")
        betterlockscreen --quiet --lock dimblur --off 30
        ;;
    "Reboot")
        reboot
        ;;
    "Shutdown")
        poweroff
        ;;
    "Sleep")
        systemctl suspend
        ;;
    *)
        exit 1
        ;;
esac
