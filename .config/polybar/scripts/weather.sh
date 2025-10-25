#!/usr/bin/env bash

# Wait for Wi-Fi connection.
sleep 100

# Cache the temperature info for 30 mins.
cache="/tmp/weather_info_cache"
if [[ -f "$cache" && $(find "$cache" -mmin -30) ]]; then
    cat "$cache"
    exit 0
fi

# Location: use city name or leave blank to auto-detect the city (not accurate).
places=("Kharghar" "Dehradun" "Dehli" "Chennai")
location="${places[0]}"

# Manually declare coords for locations.
#declare -A coords
#coords["NaviMumbai"]="19.06905,73.06924"

geo=$(curl -s "https://geocoding-api.open-meteo.com/v1/search?name=${location}&count=1" | jq -r ".results[0]")

lat=$(echo "$geo" | jq -r ".latitude")
lon=$(echo "$geo" | jq -r ".longitude")

if [[ -z "$lat" || -z "$lon" ]]; then
    echo '%{F#707880}N/A%{F-}'
    exit 0
fi

weather=$(curl -s "https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true")

temp=$(echo $weather | jq -r ".current_weather.temperature")

if [[ -z "$temp" ]]; then
    echo '%{F#707880}N/A%{F-}'
else
    echo "${temp}°C" | tee $cache
fi
