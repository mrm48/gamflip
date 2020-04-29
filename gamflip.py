import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
import gamflip_utilities
import subprocess

# Create a window with a single switch to flip the webcam
class FlipswitchWindow(Gtk.Window):

    combobox = Gtk.ComboBoxText()
    combobox_source = Gtk.ComboBoxText()

    def __init__(self):
        Gtk.Window.__init__(self, title="gamflip")
        self.set_border_width(10)

        vbox = Gtk.VBox(spacing=6)

        self.add(vbox)
        hbox = Gtk.Box(spacing=6)
        hbox2 = Gtk.Box(spacing=6)
        hbox3 = Gtk.Box(spacing=6)
        vbox.add(hbox)
        vbox.add(hbox2)
        vbox.add(hbox3)

        self.combobox = gamflip_utilities.get_dev_list(self.combobox)
        self.combobox_source = gamflip_utilities.get_dev_list(self.combobox_source)
        self.combobox_source.set_active(0)
        self.combobox.set_active(0)

        label = Gtk.Label(label="Webcam flip state:")
        hbox.pack_start(label, True, True, 0)

        flipswitch = Gtk.Switch(name="Switch")
        flipswitch.connect("notify::active", self.on_switch_activated)
        flipswitch.set_active(False)
        hbox.pack_start(flipswitch, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)
        label = Gtk.Label(label="Webcam:")
        hbox2.pack_start(label, True, True, 0)
        hbox2.pack_start(self.combobox_source, True, True, 0)
        vbox.pack_start(hbox2, True, True, 0) 
        label = Gtk.Label(label="Loopback device:")
        hbox3.pack_start(label, True, True, 0)
        hbox3.pack_start(self.combobox, True, True, 0)
        vbox.pack_start(hbox3, True, True, 0)

    def on_switch_activated(self, switch, gparam):
        if switch.get_active():
            state = "on"
            subprocess.Popen(['ffmpeg', '-f', 'v4l2', '-i', self.combobox_source.get_active_text(), '-vf', 'vflip', '-f', 'v4l2', self.combobox.get_active_text()])
        else:
            state = "off"
            subprocess.call(['killall', 'ffmpeg'])
        print("Switch was turned", state)
