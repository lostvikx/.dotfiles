#!/bin/bash

BLUETOOTH_STATUS=$(bluetoothctl show | grep "Powered" | awk '{ print $2 }')

if [ "$BLUETOOTH_STATUS" = "yes" ]; then
    bluetoothctl power off &> /dev/null
    rfkill block bluetooth
else
    rfkill unblock bluetooth
    bluetoothctl power on &> /dev/null
fi

~/.config/polybar/scripts/bluetooth_status.sh
