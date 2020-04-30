# gamflip_error.py
# If there is an error finding a dependency or a module, this class sets up the dialog to warn the user  

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

# Create a window with a single switch to flip the webcam
class GamflipErrorWindow(Gtk.Window):
    def __init__(self, dep_check, mod_check):
        Gtk.Window.__init__(self, title="gamflip")
        self.set_border_width(10)

        vbox = Gtk.VBox(spacing=6)
        self.add(vbox)

        label = Gtk.Label(label="Cannot launch, missing dependencies: " + dep_check)
        vbox.pack_start(label, True, True, 0)
        label = Gtk.Label(label="Cannot launch, missing modules: " + mod_check)
        vbox.pack_start(label, True, True, 0)