import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

# Create a window with a single switch to flip the webcam
class FlipswitchWindow(Gtk.Window):
    def __init__(self,devices):
        Gtk.Window.__init__(self, title="gamflip")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        label = Gtk.Label(label="Webcam flip state:")
        hbox.pack_start(label, True, True, 0)

        flipswitch = Gtk.Switch(name="Switch")
        flipswitch.connect("notify::active", self.on_switch_activated)
        flipswitch.set_active(False)
        hbox.pack_start(flipswitch, True, True, 0)
        label = Gtk.Label(label=devices)
        hobox.pack_start(label, True, True, 0)

    def on_switch_activated(self, switch, gparam):
        if switch.get_active():
            state = "on"
        else:
            state = "off"
        print("Switch was turned", state)