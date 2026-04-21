#!/usr/bin/env bash

# Config
CACHE_DIR="$HOME/.cache/weather"
WEATHER_CACHE="$CACHE_DIR/weather.json"
GEO_CACHE="$CACHE_DIR/geo.json"
CACHE_TTL=30  # minutes
DEFAULT_CITY="Kharghar"
UNIT="celsius"

mkdir -p "$CACHE_DIR"

# Dependencies
for cmd in curl jq; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "Error: $cmd is not installed."
        exit 1
    fi
done

# Usage: ./weather 'Navi Mumbai'
location="${1:-$DEFAULT_CITY}"

# Cache the coords for 30 days.
if [[ -f "$GEO_CACHE" ]] && \
   [[ "$(jq -r '.name' "$GEO_CACHE")" == "$location" ]] && \
   [[ $(find "$GEO_CACHE" -mtime +30 2> /dev/null) ]]; then
    lat=$(jq -r '.lat' "$GEO_CACHE")
    lon=$(jq -r '.lon' "$GEO_CACHE")
else
    geo_response=$(curl -s --connect-timeout 5 \
        "https://geocoding-api.open-meteo.com/v1/search?name=${location}&count=1")

    if [[ $? -ne 0 ]] || [[ -z "$geo_response" ]]; then
        echo "%{F#707880}N/A%{F-}"
        exit 1
    else
        lat=$(echo "$geo_response" | jq -r ".results[0].latitude // empty")
        lon=$(echo "$geo_response" | jq -r ".results[0].longitude // empty")
    fi

    if [[ -n "$lat" ]]; then
        echo "{\"name\":\"$location\", \"lat\":\"$lat\", \"lon\":\"$lon\"}" > "$GEO_CACHE"
    else
        echo "%{F#707880}N/A%{F-}"
        exit 1
    fi
fi

if [[ -f "$WEATHER_CACHE" ]] && \
   [[ $(find "$WEATHER_CACHE" -mmin -"$CACHE_TTL") ]]; then
    weather_data=$(cat "$WEATHER_CACHE")
else
    weather_data=$(curl -s --connect-timeout 5 \
        "https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&temperature_unit=${UNIT}")
    
    if [[ $? -ne 0 ]] || [[ -z "$weather_data" ]]; then
        echo "%{F#707880}N/A%{F-}"
        exit 1
    else
        echo "$weather_data" > "$WEATHER_CACHE"
    fi
fi

temp=$(echo "$weather_data" | jq -r ".current_weather.temperature")
weather_code=$(echo "$weather_data" | jq -r ".current_weather.weathercode")
is_day=$(echo "$weather_data" | jq -r ".current_weather.is_day")

# Round temperature value.
temp_int=$(printf "%.0f" "$temp")

get_icon() {
    case $1 in
        0)          ((is_day==1)) && echo "" || echo "" ;; # Clear
        1|2)        ((is_day==1)) && echo "" || echo "" ;; # Partly Cloudy
        3)          echo "" ;; # Overcast
        45|48)      echo "" ;; # Fog
        51|53|55)   echo "" ;; # Drizzle
        61|63|65)   echo "" ;; # Rain
        66|67)      echo "" ;; # Freezing Rain
        71|73|75|77)echo "" ;; # Snow
        80|81|82)   echo "" ;; # Showers
        95|96|99)   echo "" ;; # Thunder
        *)          echo "" ;; # Default
    esac
}

icon=$(get_icon "$weather_code")

if [[ -z "$temp" || "$temp" == "null" ]]; then
    echo "%{F#707880}N/A%{F-}"
else
    echo "%{T2}${icon}%{T-} ${temp_int}°C"
fi
