# gamflip_utilities.py
# Gets information for gamflip using commandline tools
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

def get_dev_list(combobox):
    devices = ""
    dev_list_output = subprocess.check_output(['v4l2-ctl', '--list-devices']).decode("utf-8")
    for device in dev_list_output.splitlines():
        if "/dev/" in device:
           combobox.append_text(device.strip()) 
    return combobox 

def execute_filters(combobox_source,combobox):
    subprocess.Popen(['ffmpeg', '-f', 'v4l2', '-i', combobox_source.get_active_text(), '-vf', 'vflip', '-f', 'v4l2', combobox.get_active_text()])

def remove_filters():
    subprocess.call(['killall', 'ffmpeg'])
