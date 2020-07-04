# main.py
# Shows the main window, unless kernel modules are not running or dependencies are not met
# TODO: Try to add support for multiple video filters

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
import gamflip_control
import gamflip_error
import subprocess


# Check for a dependency
def check_dependency(dep, dep_check):
    try:
        subprocess.check_output(['which', dep])
        return dep_check
    except:
        if len(dep_check) == 0:
            return dep
        else:
            return dep_check + ", " + dep


# Check for running modules - lsmod will error out if the module is not running
def check_module(mod):
    modules_running = subprocess.check_output(['lsmod'])
    if mod in modules_running.decode("utf-8"):
        return "all required modules found"
    else:
        return mod  

# check dependencies
dep_check = ""
dep_check = check_dependency("ffmpeg", dep_check)
dep_check = check_dependency("v4l2-ctl", dep_check)
mod_check = check_module("v4l2loopback")

# Render the window if all dependencies are met
if len(dep_check) == 0 and mod_check == "all required modules found":
    control = gamflip_control.GamflipControl()
# Show an error window with details of each dependency that isn't met    
else:
    window = gamflip_error.GamflipErrorWindow(dep_check,mod_check)
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()


