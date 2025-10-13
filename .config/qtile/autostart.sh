#!/bin/sh

dunst -config ~/.config/dunst/dunstrc &
#feh -zr ~/Pictures/walls/ --bg-fill --no-fehbg
betterlockscreen -w

picom --config ~/.config/picom/picom.conf -b
redshift -c ~/.config/redshift/redshift.conf &

batsignal -w 20 -c 10 -d 5 -b
polybar main &

xidlehook \
    --not-when-audio --not-when-fullscreen \
    --timer 300 'betterlockscreen --quiet --lock dimblur' '' &
