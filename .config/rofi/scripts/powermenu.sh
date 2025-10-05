#!/bin/sh

# More info: https://man.archlinux.org/man/extra/rofi/rofi-dmenu.5.en
ACTION=$(echo "Lock,Suspend,Reboot,Shutdown" | rofi -sep ',' -dmenu -p 'Action' -l 4)

case "$ACTION" in
    "Lock")
        betterlockscreen --quiet --lock dimblur
        ;;
    "Suspend")
        systemctl suspend
        ;;
    "Reboot")
        reboot
        ;;
    "Shutdown")
        poweroff
        ;;
    *)
        exit 1
        ;;
esac
