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

def get_dev_list():
    return subprocess.check_output(['v4l2-ctl --list-devices | grep /dev/']).decode("utf-8")