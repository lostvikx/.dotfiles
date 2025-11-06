# Note: Cross-check with default config file.

import os
import subprocess

import libqtile.resources
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# Defaults
mod: str = "mod4"  # Super Key
terminal: str = guess_terminal()
browser: str = "firefox"
file_manager: str = "thunar"

# Paths
config_path: str = os.path.expanduser("~/.config")
local_bin_path: str = os.path.expanduser("~/.local/bin")

# Keybindings
keys: list[Key] = [
    # Switch between windows.
    Key(
        [mod], "h", 
        lazy.layout.left(), 
        desc="Move focus to left."
    ),
    Key(
        [mod], "l", 
        lazy.layout.right(), 
        desc="Move focus to right."
    ),
    Key(
        [mod], "j", 
        lazy.layout.down(), 
        desc="Move focus down."
    ),
    Key(
        [mod], "k", 
        lazy.layout.up(), 
        desc="Move focus up."
    ),
    Key(
        [mod], "space", 
        lazy.layout.next(), 
        desc="Move window focus to other window."
    ),

    # Moving window to a new column or row.
    Key(
        [mod, "shift"], "h", 
        lazy.layout.shuffle_left(), 
        desc="Move window to the left."
    ),
    Key(
        [mod, "shift"], "l", 
        lazy.layout.shuffle_right(), 
        desc="Move window to the right."
    ),
    Key(
        [mod, "shift"], "j", 
        lazy.layout.shuffle_down(), 
        desc="Move window down."
    ),
    Key(
        [mod, "shift"], "k", 
        lazy.layout.shuffle_up(), 
        desc="Move window up."
    ),

    # Grow windows.
    Key(
        [mod, "control"], "h", 
        lazy.layout.grow_left(), 
        desc="Grow window to the left."
    ),
    Key(
        [mod, "control"], "l", 
        lazy.layout.grow_right(), 
        desc="Grow window to the right."
    ),
    Key(
        [mod, "control"], "j", 
        lazy.layout.grow_down(), 
        desc="Grow window down."
    ),
    Key(
        [mod, "control"], "k", 
        lazy.layout.grow_up(), 
        desc="Grow window up."
    ),
    Key(
        [mod], "n", 
        lazy.layout.normalize(), 
        desc="Reset all window sizes."
    ),

    # Toggle between split and unsplit sides of stack.
    Key(
        [mod], "s",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack."
    ),

    # Other common actions.
    Key(
        [mod, "shift"], "q", 
        lazy.window.kill(), 
        desc="Kill focused window."
    ),
    Key(
        [mod, "shift"], "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window."
    ),
    Key(
        [mod], "y", 
        lazy.window.toggle_floating(), 
        desc="Toggle floating on the focused window."
    ),
    Key(
        [mod, "control"], "r", 
        lazy.reload_config(), 
        desc="Reload the config."
    ),
    Key(
        [mod, "control"], "q", 
        lazy.shutdown(), 
        desc="Shutdown Qtile."
    ),
    Key(
        [], "Print", 
        lazy.spawn(os.path.join(local_bin_path, "capture-screenshot"), shell=True), 
        desc="Capture a screenshot."
    ),
    Key(
        [mod], "Escape", 
        lazy.spawn("betterlockscreen --lock dimblur --off 30", shell=True), 
        desc="Lock screen."
    ),

    # Launch applications.
    Key(
        [mod], "Return", 
        lazy.spawn(terminal), 
        desc="Launch terminal."
    ),
    Key(
        [mod], "b", 
        lazy.spawn(browser), 
        desc="Launch browser."
    ),
    Key(
        [mod], "f", 
        lazy.spawn(file_manager), 
        desc="Launch file manager."
    ),

    # Audio controls.
    Key(
        [], "XF86AudioMute", 
        lazy.spawn("pamixer --toggle-mute"), 
        desc="Mute audio output."
    ),
    Key(
        [], "XF86AudioLowerVolume", 
        lazy.spawn("pamixer --unmute --decrease 5"), 
        desc="Decrease audio output."
    ),
    Key(
        [], "XF86AudioRaiseVolume", 
        lazy.spawn("pamixer --unmute --increase 5"), 
        desc="Increase audio output."
    ),

    # Screen brightness control.
    # TIP: Use `brightnessctl info` to get device info.
    Key(
        [], "XF86MonBrightnessDown", 
        lazy.spawn("brightnessctl --quiet set 6000-", shell=True), 
        desc="Decrease monitor brightness."
    ),
    Key(
        [], "XF86MonBrightnessUp", 
        lazy.spawn("brightnessctl --quiet set +6000", shell=True), 
        desc="Increase monitor brightness."
    ),

    # Rofi menu system.
    Key(
        [mod], "r", 
        lazy.spawn("rofi -show drun"), 
        desc="Launch rofi menu."
    ),
    Key(
        [mod, "shift"], "r", 
        lazy.spawn("rofi -show run -no-show-icons"), 
        desc="Launch rofi to run commands."
    ),
    Key(
        [mod], "Tab", 
        lazy.spawn("rofi -show window"), 
        desc="Launch rofi to switch windows."
    ),
    Key(
        [mod, "shift"], "e",
        lazy.spawn("rofi -modi emoji -show emoji"),
        desc="Launch rofi to pick an emoji."
    ),
    Key(
        [mod, "shift"], "c",
        lazy.spawn("rofi -show calc -no-show-match -no-sort", shell=True),
        desc="Launch rofi to perform calculations."
    ),

    # Personal rofi scripts.
    Key(
        [mod, "shift"], "m", 
        lazy.spawn(os.path.join(config_path, "rofi", "scripts", "powermenu.sh"), shell=True),
        desc="Launch rofi to manage power."
    ),
    Key(
        [mod, "shift"], "p", 
        lazy.spawn(os.path.join(config_path, "rofi", "scripts", "kill.sh"), shell=True),
        desc="Launch rofi to kill a process."
    ),
    Key(
        [mod], "Print", 
        lazy.spawn(os.path.join(config_path, "rofi", "scripts", "screenshot.sh"), shell=True),
        desc="Launch rofi to take a screenshot."
    ),
]

# VTs in Wayland
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

# Workspaces (Groups)
groups: list[Group] = [Group(str(i)) for i in range(1, 6)]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod], i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}"
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"], i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}"
            ),
        ]
    )

# Layouts
margin: int = 3
wrap: bool = False

# READ: https://docs.qtile.org/en/latest/manual/ref/layouts.html#columns
layouts: list = [
    layout.Columns(
        align = 1,
        border_focus = "#cba6f7",
        border_focus_stack = "#fab387",
        border_normal = "#181825",
        border_normal_stack = "#181825",
        border_on_single = True,
        border_width = 2,
        fair = False,
        grow_amount = 10,
        initial_ratio = 1,
        insert_position = 1,
        margin = margin,
        margin_on_single = margin,
        num_columns = 2,
        single_border_width = None,
        split = True,
        wrap_focus_columns = wrap,
        wrap_focus_rows = wrap,
        wrap_focus_stacks = wrap,
    ),
]

screens: list[Screen] = [
    # Equal inner and outer margins of windows.
    Screen(
        top = bar.Gap(margin),
        right = bar.Gap(margin),
        bottom = bar.Gap(margin),
        left = bar.Gap(margin),
    ),
]

# Mouse Controls
mouse: list = [
    # Drag floating window with mod + left mouse button  hold.
    Drag(
        [mod], "Button1", 
        lazy.window.set_position_floating(), 
        start=lazy.window.get_position()
    ),
    # Resize a floating window with mod + right mouse button hold.
    Drag(
        [mod], "Button3", 
        lazy.window.set_size_floating(), 
        start=lazy.window.get_size()
    ),
    # Bring window to the front with mod + middle mouse button.
    Click(
        [mod], "Button2", 
        lazy.window.bring_to_front()
    ),
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

# Floating Windows
# TIP: Use `xprop` to get the wm_class names.
floating_layout = layout.Floating(
    border_focus = "#cba6f7",
    border_normal = "#181825",
    border_width = 2,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(wm_class="pinentry-gtk"),
    ],
    fullscreen_border_width = 0,
    max_border_width = 0,
)

# Misc
dgroups_key_binder = None
dgroups_app_rules: list = []

# Wayland Backend
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size: int = 24

# Autostart Script
@hook.subscribe.startup_once
def autostart():
    autostart_script: str = os.path.join(config_path, "qtile", "autostart.sh")
    subprocess.run([autostart_script])
