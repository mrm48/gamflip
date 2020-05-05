# gamflip_utilities.py
# Gets information for gamflip using commandline tools
import subprocess

dev_list_output = subprocess.check_output(['v4l2-ctl', '--list-devices']).decode("utf-8")

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
    for device in dev_list_output.splitlines():
        if "/dev/" in device:
           combobox.append_text(device.strip()) 
    return combobox 

def set_default_loopback(combobox):
    list_devices = subprocess.Popen(['v4l2-ctl', '--list-devices'], stdout=subprocess.PIPE)
    loopback = subprocess.Popen(['sed', '-n', '/v4l2loopback/,+1p'],stdin=list_devices.stdout,stdout=subprocess.PIPE)
    dev_loopback = subprocess.check_output(['grep', '/dev/'],stdin=loopback.stdout)
    list_devices.wait()
    loopback.wait()
    dev_loopback = dev_loopback.decode("utf-8").strip()
    combobox.append_text(dev_loopback)
    for device in dev_list_output.splitlines():
        if "/dev/" in device and device.strip() != dev_loopback:
           combobox.append_text(device.strip()) 
    return combobox 

def execute_filters(combobox_source,combobox):
    subprocess.Popen(['ffmpeg', '-f', 'v4l2', '-i', combobox_source.get_active_text(), '-vf', 'vflip', '-f', 'v4l2', combobox.get_active_text()])

def remove_filters():
    subprocess.call(['killall', '-SIGHUP', 'ffmpeg'])
