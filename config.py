# pylint: disable=W0511
"""Config de Qtile para mi escritorio"""
# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
import time
#from os import path
# Esto es para poner la hora en binario
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Screen
# esto es para definir las funciones de los espacios de trabajo.
from libqtile.config import Key, Group, Match
from libqtile.lazy import lazy
MOD = "MOD4"
TERMINAL = "alacritty"
MYBROWSER = "firefox"

def turn_off_screen():
    """Apagar pantalla"""
    subprocess.run(["xset", "dpms", "force", "off"], check=True)

# Abrir Alacritty con tmux y Ranger
def alacritty_tmux_ranger():
    """Se supone que esto servira para ejecutar la secuencia Alacritty>tmux>ranger"""
    # Abre Alacritty
    qtile.cmd_spawn('alacritty')
    # Espera 1 segundo para que Alacritty inicie
    time.sleep(1)
    # Envía la secuencia de teclas para ejecutar Tmux
    qtile.cmd_send_keys('tmux\n')
    # Espera otro segundo para que Tmux inicie
    time.sleep(1)
    # Envía la secuencia de teclas para ejecutar Ranger en Tmux
    qtile.cmd_send_keys('ranger\n')

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([MOD], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([MOD], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([MOD], "j", lazy.layout.down(), desc="Move focus down"),
    Key([MOD], "k", lazy.layout.up(), desc="Move focus up"),
    Key([MOD], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([MOD, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([MOD, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([MOD, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([MOD, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([MOD, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([MOD, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([MOD, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([MOD, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([MOD], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([MOD, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",),
    Key([MOD], "Return", lazy.spawn(TERMINAL), desc="Launch TERMINAL"),
    # Toggle between different layouts as defined below
    Key([MOD], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # Cierra ventana
    Key([MOD], "q", lazy.window.kill(), desc="Kill focused window"),
    # Recargar el fichero config.py
    Key([MOD, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([MOD, "control", "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    # Spawn el propt para llamar alguna app
    Key([MOD], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Apagar la compu
    Key([MOD, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Apagar pantalla
    Key([MOD, "shift"], "q", lazy.function(turn_off_screen), desc="turn_off_screen"),

    # LockScreen
    Key([MOD, "shift"], "b", lazy.spawn('/usr/bin/betterlockscreen -l'), desc="lockscreen"),

    #firefox
    Key([MOD], "w", lazy.spawn(MYBROWSER), desc="Spawn firefox"),

    #Neovide
    Key([MOD], "n", lazy.spawn('/usr/bin/neovide'), desc="Neovide"),

    Key([MOD, "shift"], "r", lazy.function(alacritty_tmux_ranger),
        desc="Alacritty + Tmux + Ranger"),

    # Sound
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),

    # Fullscreen toggle
    Key([MOD], "f", lazy.window.toggle_fullscreen(), desc="Toggle Fullscreen"),
    ]

groups = [Group(i) for i in "1234"]
# establece la configuración de las aplicaciones
DGROUPS_KEY_BINDER = None
dgroups_app_rules = []  # configuración de las reglas para las aplicaciones
MAIN = None

# Define una funcion para mover la ventana al espacio de trabajo correspondiente.
def move_to_group(group_name):
    """
    Mueve la ventana actual al espacio de trabajo especificado por group_name.
    :param group_name: el nombre del grupo al q se debe mover la ventana.
    """
    def _inner(client):
        client.togroup(group_name)
        client.group.cmd_toscreen()
    return _inner

for i in groups:
    # configura las reglas para las aplicaciones
    @hook.subscribe.client_new
    def assign_app_group(client):
        """Se supone q asigna una app a cada grupo, basado en su nombre de clase"""
        # establece una regla para Alacritty
        if client.window_class == "Alacritty":
            group_name = "1"
            match = Match(wm_class=["Alacritty"])
        # establece una regla para firefox
        elif client.window_class == "firefox":
            group_name = "2"
            match = Match(wm_class=["firefox"])
        # establece una regla para signal
        elif client.window_class == "signal":
            group_name = "3"
            match = Match(wm_class=["signal-desktop"])
        # establece una regla para steam y lutris
        elif client.window_class == "Lutris":
            group_name = "4"
            match = Match(wm_class=["Lutris"])
        elif client.window_class == "Steam":
            group_name = "4"
            match = Match(wm_class=["Steam"])
        else:
            return
        # mueve la ventana al espacio de trabajo correspondiente
        client.addgroup(groups[int(group_name)-1].name)
        dgroups_app_rules.append((match, move_to_group(group_name)))

    keys.extend([
        # MOD1 + letter of group = switch to group
        Key([MOD], i.name, lazy.group[i.name].toscreen(),
        desc=f"Switch to group {i.name}",),
        # MOD1 + shift + letter of group = switch to & move focused window to group
        Key([MOD, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
		desc=f"Switch to & move focused window to group {i.name}",),
        # To use rofi
        Key([MOD], "d", lazy.spawn("rofi -show run"),
            desc="Tira rofi menu"),
        Key([MOD, "shift"], "d", lazy.spawn("rofi -show filebrowser"),
            desc="Launch Rofi file browser"),

        # Or, use below if you prefer not to switch to that group.
        # # MOD1 + shift + letter of group = move focused window to group
        # Key([MOD, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
        ])

layouts = [
    layout.Columns(border_focus_stack=["#ea6962", "#b85651"],
                   border_width=2,
                   margin_on_single=0),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

## COLORS
colo = ["#282828", # background
        "#b85651", # red
        "#bd6f3e", # orange
        "#c18f41", # yellow
        "#8f9a52", # green
        "#72966c", # aqua
        "#68948a", # blue
        "#ab6c7d"] # purple

## SCREENS
# To achieve a Powerline effect without installing anything additionally, you insert Unicode
#characters ("" and "") between the widgets.
# Instead of copy-pasting the almost same lines over and over again, I used my limited Python skills
#to write this neat function.
def pline(rl_val, fg_val, bg_val):
    """Esto es para q se vea tipo Powerline, bien macizo"""
    if rl_val == 0:
        unicode_char = ""
    else:
        unicode_char = ""
    return widget.TextBox(text = unicode_char,
                          padding = 0,
                          fontsize = 12,
                          foreground=fg_val,
                          background=bg_val)

widget_defaults = {
    "font": "JetBrains Mono",
    "fontsize": 12,
    "padding": 3,
    "background": colo[0]
}
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Prompt(),
                widget.CurrentLayoutIcon(
                    scale=0.45,
                    background=colo[3]
                ),
                pline(0, colo[4], colo[3]),
                widget.Battery(
                    charge_char="now ",
                    discharge_char="left",
                    format="{percent:2.0%} {char}",
                    background=colo[4]
                    ),
                widget.Spacer(length=5),
                widget.WindowName(),
                widget.Spacer(length=bar.STRETCH),
                widget.GroupBox(
                    highlight_method="block",
                    background=colo[6],
                    this_current_screen_border="#7daea3"
                ),
                widget.Spacer(length=bar.STRETCH),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                #widget.StatusNotifier(),
                widget.Net(
                    interface="wlo1",
                    format="📡 {total}",
                    update_interval=30,
                    background=colo[4]
                ),
                widget.Systray(),
                widget.Spacer(length=10),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p", background=colo[3]),
                #widget.QuickExit(),
            ],
            24, #Esta es la altura de la barra.
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]
# Drag floating layouts.
mouse = [
    Drag([MOD], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([MOD], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
]

DGROUPS_KEY_BINDER = None
dgroups_app_rules = []  # type: list
FOLLOW_MOUSE_FOCUS = True
BRING_FRONT_CLICK = False
CURSOR_WARP = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
AUTO_FULLSCREEN = True
FOCUS_ON_WINDOW_ACTIVATION = "smart"
RECONFIGURE_SCREENS = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
AUTO_MINIMIZE = True

# When using the Wayland backend, this can be used to configure input devices.
WL_INPUT_RULES = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
WMNAME = "LG3D"

## AUTOSTART
@hook.subscribe.startup
def autostart():
    """bueno aqui se supone q se ejecuta el nitrogen y cualquier vrga q le ponga al autostart"""
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])
