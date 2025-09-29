#!/bin/bash

BLUETOOTH_STATUS=$(bluetoothctl show | grep "Powered" | awk '{ print $2 }')

if [ "$BLUETOOTH_STATUS" = "yes" ]; then
    echo "󰂯 On"
else
    echo '%{F#707880}󰂲 Off%{F-}'
fi
