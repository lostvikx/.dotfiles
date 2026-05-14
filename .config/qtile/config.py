# Note: Cross-check with default config file.

import os
import subprocess
from collections.abc import Callable

import libqtile.resources
from helper import get_battery, get_volume, get_wifi_icon, trim_window_name
from libqtile import bar, hook, layout, qtile, widget
from libqtile.backend.wayland.inputs import InputConfig
from libqtile.config import (
    Click,
    Drag,
    Group,
    IdleInhibitor,
    IdleTimer,
    Key,
    Match,
    Output,
    Screen,
)
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import backlight

mod: str = "mod4"  # Super Key
is_wayland: bool = qtile.core.name == "wayland"

# Default Apps
browser: str = "firefox"
file_manager: str = "thunar"

terminal: str = guess_terminal() or "kitty"

if is_wayland:
    terminal = "foot"


# Paths
config_path: str = os.path.expanduser("~/.config")
local_bin_path: str = os.path.expanduser("~/.local/bin")


# Keybindings
# DOCS: https://docs.qtile.org/en/latest/manual/config/lazy.html
keys: list[Key] = [
    # Switch between windows.
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left."),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right."),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down."),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up."),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window."),
    # Moving window to a new column or row.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left."
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right.",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down."),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up."),
    # Grow windows.
    Key(
        [mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left."
    ),
    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        desc="Grow window to the right.",
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down."),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up."),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes."),
    # Toggle between split and unsplit sides of stack.
    Key(
        [mod],
        "s",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack.",
    ),
    # Other common actions.
    Key([mod], "z", lazy.next_layout(), desc="Toggle between layouts."),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window."),
    Key(
        [mod, "shift"],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window.",
    ),
    Key(
        [mod],
        "y",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window.",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config."),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile."),
    Key(
        [],
        "Print",
        lazy.spawn(os.path.join(local_bin_path, "capture-screenshot"), shell=True),
        desc="Capture a screenshot.",
    ),
    # TODO: Wayland
    Key(
        [mod],
        "Escape",
        lazy.spawn("betterlockscreen --lock dimblur --off 30", shell=True),
        desc="Lock screen.",
    ),
    # Launch applications.
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal."),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser."),
    Key([mod], "f", lazy.spawn(file_manager), desc="Launch file manager."),
    # Audio controls.
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("pamixer --toggle-mute"),
        desc="Mute audio output.",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pamixer --unmute --decrease 5"),
        desc="Decrease audio output.",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pamixer --unmute --increase 5"),
        desc="Increase audio output.",
    ),
    # Screen brightness control.
    # TIP: Use `brightnessctl info` to get device info.
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl --quiet set 6000-", shell=True),
        lazy.widget["backlight"].change_backlight(backlight.ChangeDirection.DOWN),
        desc="Decrease monitor brightness.",
    ),
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl --quiet set +6000", shell=True),
        lazy.widget["backlight"].change_backlight(backlight.ChangeDirection.UP),
        desc="Increase monitor brightness.",
    ),
]


if is_wayland:
    keys.extend(
        [
            Key([mod], "r", lazy.spawn("fuzzel"), desc="Launch fuzzel menu."),
        ]
    )
else:
    # Menu: rofi
    keys.extend(
        [
            Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Launch rofi menu."),
            Key(
                [mod, "shift"],
                "r",
                lazy.spawn("rofi -show run -no-show-icons"),
                desc="Launch rofi to run commands.",
            ),
            Key(
                [mod],
                "Tab",
                lazy.spawn("rofi -show window"),
                desc="Launch rofi to switch windows.",
            ),
            Key(
                [mod, "shift"],
                "e",
                lazy.spawn("rofi -modi emoji -show emoji"),
                desc="Launch rofi to pick an emoji.",
            ),
            Key(
                [mod, "shift"],
                "c",
                lazy.spawn("rofi -show calc -no-show-match -no-sort", shell=True),
                desc="Launch rofi to perform calculations.",
            ),
            # Personal rofi scripts.
            Key(
                [mod, "shift"],
                "m",
                lazy.spawn(
                    os.path.join(config_path, "rofi", "scripts", "powermenu.sh"),
                    shell=True,
                ),
                desc="Launch rofi to manage power.",
            ),
            Key(
                [mod, "shift"],
                "p",
                lazy.spawn(
                    os.path.join(config_path, "rofi", "scripts", "kill.sh"), shell=True
                ),
                desc="Launch rofi to kill a process.",
            ),
            Key(
                [mod],
                "Print",
                lazy.spawn(
                    os.path.join(config_path, "rofi", "scripts", "screenshot.sh"),
                    shell=True,
                ),
                desc="Launch rofi to take a screenshot.",
            ),
        ]
    )


# VTs in Wayland
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: is_wayland),
            desc=f"Switch to VT{vt}",
        )
    )


# Workspaces (Groups)
groups: list[Group] = []

# TODO: Wayland
# Install wlr-randr
# n_monitors: int = sum(
#     " connected" in line and "+" in line
#     for line in subprocess.check_output(["xrandr"]).decode().splitlines()
# )
n_monitors = 1

if n_monitors == 2:
    # Multi-Monitor Setup
    pinned_groups: list[str] = ["12345", "67890"]
    all_groups: str = "".join(pinned_groups)

    groups = [Group(i) for i in all_groups]

    for screen_idx, names in enumerate(pinned_groups):
        for i in names:
            keys.append(
                Key(
                    [mod],
                    i,
                    lazy.to_screen(screen_idx),
                    lazy.group[i].toscreen(toggle=False),
                    desc=f"Switch monitor and switch to group {i}",
                )
            )

    keys.extend(
        Key([mod, "shift"], i, lazy.window.togroup(i, switch_group=False))
        for i in all_groups
    )
else:
    groups = [Group(str(i)) for i in range(1, 6)]

    for i in groups:
        keys.extend(
            [
                # mod + group number = switch to group
                Key(
                    [mod],
                    i.name,
                    lazy.group[i.name].toscreen(),
                    desc=f"Switch to group {i.name}",
                ),
                # mod + shift + group number = switch to & move focused window to group
                Key(
                    [mod, "shift"],
                    i.name,
                    lazy.window.togroup(i.name, switch_group=True),
                    desc=f"Switch to & move focused window to group {i.name}",
                ),
            ]
        )


# Layouts
border_width: int = 2
colors: dict = {"primary": "#cba6f7", "secondary": "#fab387", "dark": "#181825"}
margin: int = 3
wrap: bool = False


# Floating Windows
# TIP: Use `xprop` or `wlprop` to get the wm_class names.

floating_layout = layout.Floating(
    border_focus=colors.get("primary"),
    border_normal=colors.get("dark"),
    border_width=border_width,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(wm_class="pinentry-gtk"),
    ],
    fullscreen_border_width=0,
    max_border_width=0,
)

# DOCS: https://docs.qtile.org/en/latest/manual/ref/layouts.html#columns
layouts: list = [
    layout.Columns(
        align=1,
        border_focus=colors.get("primary"),
        border_focus_stack=colors.get("secondary"),
        border_normal=colors.get("dark"),
        border_normal_stack=colors.get("dark"),
        border_on_single=True,
        border_width=border_width,
        fair=False,
        grow_amount=10,
        initial_ratio=1,
        insert_position=1,
        margin=margin,
        margin_on_single=margin,
        num_columns=2,
        single_border_width=None,
        split=True,
        wrap_focus_columns=wrap,
        wrap_focus_rows=wrap,
        wrap_focus_stacks=wrap,
    ),
    layout.Floating(
        border_focus=colors.get("primary"),
        border_normal=colors.get("dark"),
        border_width=border_width,
    ),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=15,
    foreground="#CDD6F4",
    background="#1E1E2E",
    padding=margin + 3,
)
extension_defaults = widget_defaults.copy()
logo = os.path.join(os.path.dirname(libqtile.resources.__file__), "logo.png")

mocha = dict(
    background=widget_defaults["background"],
    background_alt="#313244",
    foreground=widget_defaults["foreground"],
    primary="#CBA6F7",
    secondary="#F5C2E7",
    alert="#F38BA8",
    disabled="#6C7086",
)

separator = widget.Sep(padding=18, linewidth=border_width, foreground=mocha["disabled"])
menu = widget.TextBox(
    text="󰣇",
    foreground=mocha["primary"],
    padding=6,
    mouse_callbacks={"Button1": lazy.spawn("fuzzel")},
)


bottom_bar = bar.Bar(
    widgets=[
        # menu,
        widget.GroupBox(
            active=mocha["foreground"],
            disable_drag=True,
            block_highlight_text_color=mocha["primary"],
            highlight_color=[mocha["background_alt"], "282828"],
            highlight_method="line",
            inactive=mocha["disabled"],
            other_current_screen_border=mocha["disabled"],
            this_current_screen_border=mocha["primary"],
            this_screen_border=mocha["primary"],
            urgent_alert_method="line",
            urgent_border=mocha["alert"],
            urgent_text=mocha["alert"],
            use_mouse_wheel=False,
        ),
        separator,
        widget.WindowName(
            empty_group_string="No Active Window",
            parse_text=trim_window_name,
        ),
        widget.StatusNotifier(icon_theme="Papirus"),
        separator,
        widget.ThermalZone(
            crit=80,
            format=" {temp}°C",
            format_crit=" {temp}°C",
            high=70,
            update_interval=60,
            fgcolor_normal=mocha["foreground"],
            fgcolor_high=mocha["secondary"],
            fgcolor_crit=mocha["alert"],
        ),
        separator,
        widget.GenPollText(func=get_wifi_icon, update_interval=30),
        widget.WlanIw(disconnected_message="No Wi-Fi", format="{essid}"),
        separator,
        widget.Backlight(format="󰛩 {percent:2.0%}"),
        separator,
        # widget.TextBox(text="󰕾"),
        # widget.Volume(),
        # widget.GenPollText(func=get_volume, update_interval=0.2),
        # widget.PulseVolume(),
        # separator,
        widget.GenPollText(func=get_battery, update_interval=30),
        separator,
        widget.Clock(format="%a %b %d %H:%M"),
    ],
    size=26,
    margin=[margin, 0, 0, 0],  # Fixed
)


screens = []
for i in range(n_monitors):
    screens.append(
        Screen(
            top=bar.Gap(margin),
            right=bar.Gap(margin),
            bottom=bottom_bar if is_wayland else bar.Gap(margin),
            left=bar.Gap(margin),
        )
    )

fake_screens: list[Screen]
generate_screens: Callable[[list[Output]], list[Screen]]

# Mouse Controls
mouse: list = [
    # Drag floating window with mod + left mouse button hold.
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    # Resize a floating window with mod + right mouse button hold.
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    # Bring window to the front with mod + middle mouse button.
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

follow_mouse_focus: bool = False
bring_front_click: bool = False
floats_kept_above: bool = True
cursor_warp: bool = False


# Windows
wmname: str = "qtile"
auto_fullscreen: bool = True
focus_on_window_activation: str = "smart"
focus_previous_on_window_remove: bool = False
reconfigure_screens: bool = True
auto_minimize: bool = True


# Misc
dgroups_key_binder = None
dgroups_app_rules: list = []


# Wayland Backend
wl_input_rules = {
    "type:touchpad": InputConfig(tap=True, natural_scroll=True),
    "type:keyboard": InputConfig(kb_layout="us"),
}
wl_xcursor_theme = None
wl_xcursor_size: int = 24

# Idle Events
idle_timers: list[IdleTimer] = []
idle_inhibitors: list[IdleInhibitor] = []


@hook.subscribe.startup_once
def autostart():
    autostart_script: str
    if is_wayland:
        autostart_script = os.path.join(
            config_path, "qtile", "scripts", "autostart_wl.sh"
        )
    else:
        autostart_script = os.path.join(
            config_path, "qtile", "scripts", "autostart_x11.sh"
        )

    subprocess.run([autostart_script])
