# gamflip_control.py
# Shows the main window, unless there is no camera, kernel modules are not running or dependencies are not met

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
import gamflip
import gamflip_utilities
import gamflip_error
import subprocess
import os

class GamflipControl():

    utilities = gamflip_utilities.GamflipUtilities()

    def __init__(self):
        # check dependencies
        dep_check = ""
        dep_check = self.check_dependency("ffmpeg", dep_check)
        dep_check = self.check_dependency("v4l2-ctl", dep_check)
        mod_check = self.check_module("v4l2loopback")
        cam_check = self.check_camera()
    
        # Render the window if all dependencies are met
        if len(dep_check) == 0 and mod_check == "all required modules found":
            window = gamflip.FlipswitchWindow()
            window.connect("destroy", window.cleanup)
            window.show_all()
            window.show_warning(gparam="")
            Gtk.main()
        else:
            window = gamflip_error.GamflipErrorWindow(cam_check,dep_check,mod_check)
            window.connect("destroy", Gtk.main_quit)
            window.show_all()
            Gtk.main()

    # Check for a dependency
    def check_dependency(self, dep, dep_check):
        try:
            subprocess.check_output(['which', dep])
            return dep_check
        except:
            if len(dep_check) == 0:
                return dep
            else:
                return dep_check + ", " + dep


    # Check for running modules - lsmod will error out if the module is not running
    def check_module(self, mod):
        modules_running = subprocess.check_output(['lsmod'])
        if mod in modules_running.decode("utf-8"):
            return "all required modules found"
        else:
            return mod  
    
    def check_camera(self):
        if os.path.exists("/dev/video0") != True:
            #self.init_output = "No webcam found"
            return "Not found"
        else:
            return "Found"
