#!/bin/sh

dunst -config ~/.config/dunst/dunstrc &
swaybg -i ~/Pictures/background.jpg -m fill &
wlsunset -l 19.07 -L 72.87 &
batsignal -w 20 -c 10 -b

swayidle -w \
    timeout 300 'swaylock -f -i ~/Pictures/lockscreen.jpg' \
    timeout 600 'swaymsg "output * dpms off"' \
    resume 'swaymsg "output * dpms on"' &
