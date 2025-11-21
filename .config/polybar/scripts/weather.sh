#!/usr/bin/env bash

# Wait for Wi-Fi connection.
sleep 100

# Cache the temperature info for 30 mins.
cache="/tmp/weather.cache"
if [[ -f "$cache" && $(find "$cache" -mmin -30) ]]; then
    cat "$cache"
    exit 0
fi

# Location: use city or locality name
places=("Kharghar" "Dehradun" "Delhi" "Chennai")
location="${places[0]}"

geo=$(curl -s "https://geocoding-api.open-meteo.com/v1/search?name=${location}&count=1" | jq -r ".results[0]")

lat=$(echo "$geo" | jq -r ".latitude")
lon=$(echo "$geo" | jq -r ".longitude")

if [[ -z "$lat" || -z "$lon" ]]; then
    echo '%{F#707880}N/A%{F-}'
    exit 0
fi

weather=$(curl -s "https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true")

temp=$(echo $weather | jq -r ".current_weather.temperature")
weather_code=$(echo $weather | jq -r ".current_weather.weathercode")
is_day=$(echo $weather | jq -r ".current_weather.is_day")

get_icon() {
    case $1 in
        0) 
            [[ "$is_day" -eq 1 ]] && echo "" || echo ""
            ;;     # Clear sky
        1|2) echo "" ;;   # Partly cloudy
        3) echo "" ;;     # Cloudy
        45|48) echo "" ;; # Fog
        51|53|55) echo "" ;; # Drizzle
        56|57|61|63|65) echo "" ;; # Rain
        66|67) echo "" ;; # Freezing rain
        71|73|75|77) echo "" ;; # Snow
        95|96|99) echo "" ;; # Thunder
        *) echo "" ;;    # Default (unknown)
    esac
}

icon=$(get_icon "$weather_code")

if [[ -z "$temp" ]]; then
    echo '%{F#707880}N/A%{F-}'
else
    echo "${icon} ${temp}°C" | tee $cache
fi
