#!/bin/bash

#BLUETOOTH_STATUS=$(bluetoothctl show | grep "Powered" | awk '{ print $2 }')
BLUETOOTH_STATUS=$(bluetooth | awk '{ print $3 }')

if [ "$BLUETOOTH_STATUS" = "on" ]; then
    echo "󰂯 On"
else
    echo '%{F#707880}󰂲 Off%{F-}'
fi
