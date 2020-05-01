# main.py
# Shows the main window, unless kernel modules are not running or dependencies are not met

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
import gamflip
import gamflip_utilities
import gamflip_error

# check dependencies
dep_check = ""
dep_check = gamflip_utilities.check_dependency("ffmpeg", dep_check)
dep_check = gamflip_utilities.check_dependency("v4l2-ctl", dep_check)
mod_check = gamflip_utilities.check_module("v4l2loopback")

# Render the window if all dependencies are met
if len(dep_check) == 0 and mod_check == "all required modules found":

    window = gamflip.FlipswitchWindow()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
    
else:
    window = gamflip_error.GamflipErrorWindow(dep_check,mod_check)
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
