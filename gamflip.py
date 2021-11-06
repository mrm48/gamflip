# gamflip.py
# Contains the main window class and is responsible for populating it

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gio
import gamflip_utilities

# Create a window with a single switch to flip the webcam
class FlipswitchWindow(Gtk.Window):

    # Setup widgets that user will interact with
    combobox = Gtk.ComboBoxText()
    combobox_source = Gtk.ComboBoxText()
    flipswitch = Gtk.Switch(name="Switch")
    greyswitch = Gtk.Switch(name="GreySwitch")
    warning = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="dialog-warning-symbolic"),Gtk.IconSize.BUTTON)
    warning.set_tooltip_text("No webcam is installed or loopback is the same device, please use v4l2-ctl --list-devices to determine which devices to use.")
    utilities = gamflip_utilities.GamflipUtilities()
    
    def __init__(self):

        # Create Window and Grid
        Gtk.Window.__init__(self, title="gamflip")
        self.set_border_width(10)

        grid = Gtk.Grid()
        self.add(grid)

        # Create and add devices to dropdowns
        self.combobox = self.utilities.set_default_loopback(self.combobox)
        self.combobox_source = self.utilities.get_dev_list(self.combobox_source)
        self.combobox_source.set_active(0)
        self.combobox.set_active(0)

        # Row 1 (Flip cam switch)
        label1 = Gtk.Label(label="Flip")
        label1.set_margin_bottom(10)
        grid.add(label1)
        self.warning.set_margin_left(35)
        self.warning.set_margin_bottom(10)
        grid.attach_next_to(self.warning,label1,Gtk.PositionType.RIGHT,1,1)
        self.flipswitch.set_margin_left(10)
        self.flipswitch.set_margin_right(15)
        self.flipswitch.set_margin_bottom(10)
        self.flipswitch.set_hexpand(False)
        self.flipswitch.set_hexpand_set(True)
        self.flipswitch.connect("notify::active", self.on_switch_activated)
        self.flipswitch.set_active(False)
        grid.attach_next_to(self.flipswitch,self.warning,Gtk.PositionType.RIGHT,2,1)

        # Row 2 (Greyscale switch)
        label_greyswitch = Gtk.Label(label="Greyscale")
        label_greyswitch.set_margin_bottom(10)
        grid.attach_next_to(label_greyswitch,label1,Gtk.PositionType.BOTTOM,1,2)
        self.greyswitch.set_margin_left(135)
        self.greyswitch.set_margin_right(15)
        self.greyswitch.set_margin_bottom(10)
        self.greyswitch.set_hexpand(False)
        self.greyswitch.set_hexpand_set(True)
        self.greyswitch.connect("notify::active", self.on_switch_activated)
        self.greyswitch.set_active(False)
        grid.attach_next_to(self.greyswitch,label_greyswitch,Gtk.PositionType.RIGHT,2,2)
        
        # Row 3 - Source (Webcam)
        label2 = Gtk.Label(label="Webcam")
        label2.set_margin_bottom(5)
        self.combobox_source.set_margin_bottom(5)
        self.combobox_source.set_margin_left(25)
        self.combobox_source.connect("changed", self.show_warning)
        grid.attach_next_to(label2,label_greyswitch,Gtk.PositionType.BOTTOM,1,2)
        grid.attach_next_to(self.combobox_source,label2,Gtk.PositionType.RIGHT,2,1)
        
        # Row 4 - Loopback Device
        label3 = Gtk.Label(label="Loopback device")
        grid.attach_next_to(label3,label2,Gtk.PositionType.BOTTOM,1,2)
        self.combobox.set_margin_left(25)
        self.combobox.connect("changed", self.show_warning)
        grid.attach_next_to(self.combobox,label3,Gtk.PositionType.RIGHT,2,1)

    # Action while flipping switch
    # On: Use ffmpeg to flip the video
    # Off: clean up running ffmpeg process
    def on_switch_activated(self, switch, gparam):
        self.utilities.execute_filters(flip=self.flipswitch.get_active(), grey=self.greyswitch.get_active(), source=self.combobox_source.get_active_text(), loopback=self.combobox.get_active_text())

    def cleanup(self, destroy):
        self.utilities.remove_filters()
        Gtk.main_quit()

    def show_warning(self,gparam):
        if self.combobox_source.get_active_text() == self.combobox.get_active_text() or self.combobox_source.get_active_text() == None:
            self.warning.show()
            self.flipswitch.set_sensitive(False)
            self.greyswitch.set_sensitive(False)
        else:
            self.warning.hide()
            self.flipswitch.set_sensitive(True)
            self.greyswitch.set_sensitive(True)
            self.flipswitch.set_halign(Gtk.Align.END)



