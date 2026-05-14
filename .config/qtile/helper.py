import subprocess


def get_wifi_icon():
    try:
        output = subprocess.check_output("iw dev wlan0 link", shell=True).decode()

        if "signal" not in output:
            return "󰤭 Disconnected"

        signal = int(output.split("signal:")[1].split("dBm")[0].strip())

        # Convert dBm to %
        percent = max(0, min(100, 2 * (signal + 100)))

        if percent > 80:
            icon = "󰤨"
        elif percent > 60:
            icon = "󰤥"
        elif percent > 40:
            icon = "󰤢"
        elif percent > 20:
            icon = "󰤟"
        else:
            icon = "󰤯"

        return f"{icon}"

    except Exception:
        return "󰤭"


def get_battery():
    try:
        base = "/sys/class/power_supply/BAT0/"

        with open(base + "capacity") as f:
            percent = int(f.read().strip())

        with open(base + "status") as f:
            status = f.read().strip().lower()

        charging = status == "charging"

        if charging:
            icon = "󰂄"
        elif percent > 80:
            icon = "󰁹"
        elif percent > 60:
            icon = "󰂂"
        elif percent > 40:
            icon = "󰂀"
        elif percent > 20:
            icon = "󰁾"
        else:
            icon = "󰁺"

        return f"{icon} {percent}%"

    except Exception:
        return "󰂃"


def trim_window_name(text: str) -> str:
    for unwanted in [" — Mozilla Firefox", " — Chromium"]:
        text = text.replace(unwanted, "")

    if len(text) > 50:
        return text[:47] + "..."

    return text


def get_volume():
    try:
        vol = int(subprocess.check_output(["pamixer", "--get-volume"]).decode().strip())

        mute = (
            subprocess.check_output(["pamixer", "--get-mute"]).decode().strip()
            == "true"
        )

        if mute:
            return "󰖁 Mute"

        # Icon levels (Nerd Fonts)
        if vol == 0:
            icon = "󰕿"  # muted/zero
        elif vol < 30:
            icon = "󰖀"  # low
        elif vol < 70:
            icon = "󰕾"  # medium
        else:
            icon = "󰕾"  # high (you can swap if you prefer louder icon)

        return f"{icon} {vol}%"

    except Exception:
        return "?"
