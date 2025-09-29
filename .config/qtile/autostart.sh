#!/bin/sh

feh -zr ~/Pictures/walls/ --bg-scale
#picom --experimental-backends --config ~/.config/picom/picom.conf -b

picom --config ~/.config/picom/picom.conf -b
redshift -c ~/.config/redshift/redshift.conf &

# Polybar
killall -q polybar

while pgrep -u $UID -x polybar >/dev/null; do 
    sleep 1
done

polybar main &
