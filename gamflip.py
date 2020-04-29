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

        # Create Window and Grid
        Gtk.Window.__init__(self, title="gamflip")
        self.set_border_width(10)

        grid = Gtk.Grid()
        self.add(grid)

        # Create and add devices to dropdowns
        self.combobox = gamflip_utilities.get_dev_list(self.combobox)
        self.combobox_source = gamflip_utilities.get_dev_list(self.combobox_source)
        self.combobox_source.set_active(0)
        self.combobox.set_active(0)

        # Row 1 (Switch)
        label1 = Gtk.Label(label="Webcam flip state:")
        label1.set_margin_bottom(10)
        grid.add(label1)
        flipswitch = Gtk.Switch(name="Switch")
        flipswitch.set_margin_left(50)
        flipswitch.set_margin_right(50)
        flipswitch.set_margin_bottom(10)
        flipswitch.connect("notify::active", self.on_switch_activated)
        flipswitch.set_active(False)
        grid.attach_next_to(flipswitch,label1,Gtk.PositionType.RIGHT,3,1)
        
        # Row 2 - Source (Webcam)
        label2 = Gtk.Label(label="Webcam:")
        label2.set_margin_bottom(10)
        self.combobox_source.set_margin_bottom(10)
        grid.attach_next_to(label2,label1,Gtk.PositionType.BOTTOM,1,2)
        grid.attach_next_to(self.combobox_source,label2,Gtk.PositionType.RIGHT,2,1)
        
        # Row 3 - Loopback Device
        label3 = Gtk.Label(label="Loopback device:")
        grid.attach_next_to(label3,label2,Gtk.PositionType.BOTTOM,1,2)
        grid.attach_next_to(self.combobox,label3,Gtk.PositionType.RIGHT,2,1)

    def on_switch_activated(self, switch, gparam):
        if switch.get_active():
            state = "on"
            subprocess.Popen(['ffmpeg', '-f', 'v4l2', '-i', self.combobox_source.get_active_text(), '-vf', 'vflip', '-f', 'v4l2', self.combobox.get_active_text()])
        else:
            state = "off"
            subprocess.call(['killall', 'ffmpeg'])
        print("Switch was turned", state)
