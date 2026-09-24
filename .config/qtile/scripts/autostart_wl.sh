#!/bin/sh

dunst -config ~/.config/dunst/dunstrc &
#swaybg -i ~/Pictures/background.png -m fill &
swaybg -i ~/Pictures/background.jpg -m center -c '#11111b' &
wlsunset -T 6500 -t 3500 -S 05:00 -s 21:00 -d 3600 &
batsignal -w 20 -c 10 -b

#swayidle -w \
#    timeout 300 'swaylock -f -i "$HOME/Pictures/lockscreen.jpg"' \
#    timeout 360 'wlr-randr --output eDP-1 --off' \
#    resume 'wlr-randr --output eDP-1 --on' &

#swayidle -w \
#    timeout 300 'swaylock -f -i "$HOME/Pictures/lockscreen.jpg"' \
#    timeout 360 'wlr-randr --output eDP-1 --off' \
#    resume 'wlr-randr --output eDP-1 --on' \
#    before-sleep 'swaylock -f -i "$HOME/Pictures/lockscreen.jpg"' \
#    after-resume 'wlr-randr --output eDP-1 --on' &
