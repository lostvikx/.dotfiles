#!/bin/sh

dunst -config ~/.config/dunst/dunstrc &

# set the wallpaper
betterlockscreen --wall
#feh -zr ~/Pictures/walls/ --bg-fill --no-fehbg  # random wallpaper

picom --config ~/.config/picom/picom.conf -b
redshift -c ~/.config/redshift/redshift.conf &

batsignal -w 20 -c 10 -d 5 -b
polybar main &

xset s off -dpms

#xidlehook --not-when-audio --not-when-fullscreen --timer 300 'betterlockscreen --quiet --lock dimblur' '' &
