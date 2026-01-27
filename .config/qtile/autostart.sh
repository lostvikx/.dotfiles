#!/bin/sh

dunst -config ~/.config/dunst/dunstrc &

# set the wallpaper
betterlockscreen --wall
#feh -zr ~/Pictures/walls/ --bg-fill --no-fehbg  # random wallpaper

picom --config ~/.config/picom/picom.conf -b
redshift -c ~/.config/redshift/redshift.conf &

batsignal -w 20 -c 10 -b
polybar main &

xset s off -dpms
xset r rate 600 25
# xset r rate 660 25  # default settings

#xidlehook --not-when-audio --not-when-fullscreen --timer 300 'betterlockscreen --quiet --lock dimblur' '' &
