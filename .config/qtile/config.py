# NOTE: I have removed all configs related to wayland.

import os
import subprocess

import libqtile.resources
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# Super Key
mod = "mod4"

# Default Apps
terminal = guess_terminal()
browser = "firefox"
file_manager = "thunar"

# Keybindings
keys = [
    # Switch between windows.
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left."),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right."),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down."),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up."),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window."),

    # Moving window to a new column or row.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left."),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right."),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down."),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up."),

    # Grow windows.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left."),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right."),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down."),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up."),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes."),

    # Toggle between split and unsplit sides of stack.
    Key(
        [mod], "s",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack."
    ),

    # Other common actions.
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window."),
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
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config."),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile."),

    # Launch applications.
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal."),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser."),
    Key([mod], "f", lazy.spawn(file_manager), desc="Launch file manager."),

    Key([mod], "Escape", lazy.spawn("betterlockscreen --quiet --lock dimblur", shell=True), desc="Lock screen."),

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
    Key(
        [], "XF86MonBrightnessDown", 
        lazy.spawn("brightnessctl set 5%-"), 
        desc="Decrease monitor brightness."
    ),
    Key(
        [], "XF86MonBrightnessUp", 
        lazy.spawn("brightnessctl set +5%"), 
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
        [mod], "c",
        lazy.spawn("rofi -show calc -no-show-match -no-sort", shell=True),
        desc="Launch rofi to perform calculations."
    ),
    Key(
        [mod], "l", 
        lazy.spawn("/home/vik/.config/rofi/scripts/powermenu.sh", shell=True), 
        desc="Launch rofi to manage power."
    ),
    Key(
        [mod], "k", 
        lazy.spawn("/home/vik/.config/rofi/scripts/kill.sh", shell=True), 
        desc="Launch rofi to kill a process."
    ),

    # Taking screenshots of display.
    Key(
        [], "Print", 
        lazy.spawn("maim --noopengl -s | xclip -selection clipboard -t image/png", shell=True),
        desc="Screenshot selection to clipboard."
    ),
    Key(
        ["shift"], "Print", 
        lazy.spawn("maim --noopengl ~/Pictures/Screenshots/$(date +%Y-%m-%d_%H-%M-%S).png", shell=True),
        desc="Screenshot fullscreen to file."
    ),
    Key(
        ["control"], "Print", 
        lazy.spawn("maim --noopengl | xclip -selection clipboard -t image/png", shell=True),
        desc="Screenshot fullscreen to clipboard."
    ),
]

# Workspaces (Groups)
groups = [Group(i) for i in "12345"]

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
margin = 3

layouts = [
    # NOTE: Check out the docs: https://docs.qtile.org/en/latest/manual/ref/layouts.html#columns
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
        wrap_focus_columns = True,
        wrap_focus_rows = True,
        wrap_focus_stacks = True,
    ),
]

screens = [
    # Equal inner and outer margins of windows.
    Screen(
        top = bar.Gap(margin),
        right = bar.Gap(margin),
        bottom = bar.Gap(margin),
        left = bar.Gap(margin),
    ),
]

# Mouse Controls
mouse = [
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
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = False

# Windows
wmname = "qtile"
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True
auto_minimize = True

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
dgroups_app_rules = []  # type: list

wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24

# Autostart Script
@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([script])
