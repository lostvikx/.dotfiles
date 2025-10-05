#!/bin/sh

PID=$(ps -a -u $USER | awk 'NR > 1 { print $1, $4 }' | rofi -dmenu -p 'Kill' -mesg 'PID CMD' -no-show-icons | awk '{ print $1 }')

if [ -n "$PID" ]; then
    kill -9 "$PID"
fi
