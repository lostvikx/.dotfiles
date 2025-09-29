#!/bin/sh

feh -zr ~/Pictures/walls/ --bg-fill

picom --config ~/.config/picom/picom.conf -b
redshift -c ~/.config/redshift/redshift.conf &

# polybar
killall -q polybar

while pgrep -u $UID -x polybar >/dev/null; do 
    sleep 1
done

polybar main &
