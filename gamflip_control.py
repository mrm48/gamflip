# main.py
# Shows the main window, unless kernel modules are not running or dependencies are not met
# TODO: Try to add support for multiple video filters

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
import gamflip
import gamflip_utilities
import gamflip_error

class GamflipControl():

    def __init__(self):
        utilities = gamflip_utilities.GamflipUtilities()
        window = gamflip.FlipswitchWindow()
        window.connect("destroy", window.cleanup)
        window.show_all()
        window.show_warning(gparam="")
        Gtk.main()

