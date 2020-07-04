# main.py
# Shows the main window, unless kernel modules are not running or dependencies are not met
# TODO: Try to add support for multiple video filters

# import gi
# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk
# from gi.repository import GLib
import gamflip_control


control = gamflip_control.GamflipControl()


