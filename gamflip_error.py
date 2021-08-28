# gamflip_error.py
# If there is an error finding a dependency or a module, this class sets up the dialog to warn the user  

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

# Create a window with a single switch to flip the webcam
class GamflipErrorWindow(Gtk.Window):
    def __init__(self, cam_check, dep_check, mod_check):
        Gtk.Window.__init__(self, title="gamflip")
        self.set_border_width(10)

        vbox = Gtk.VBox(spacing=6)
        self.add(vbox)

        # Check for the camera, otherwise, let the user know the webcam is not detected
        if cam_check == "Found":
            label = Gtk.Label(label="Camera: Detected")
        else:
            label = Gtk.Label(label="Camera: Not detected")

        vbox.pack_start(label, True, True, 0)

        # Check for programs listed as dependencies (v4l-ctl and ffmpeg), otherwise let user know what is missing
        if dep_check == "Found":
            label = Gtk.Label(label="All dependencies found")
        else:
            label = Gtk.Label(label="Cannot launch, missing dependencies: " + dep_check)

        vbox.pack_start(label, True, True, 0)

        # Check for kernel modules
        if mod_check == "Found":
            label = Gtk.Label(label="All modules found")
        else:
            label = Gtk.Label(label="Cannot launch, missing modules: " + mod_check)

        vbox.pack_start(label, True, True, 0)
