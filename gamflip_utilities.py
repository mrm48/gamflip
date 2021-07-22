# gamflip_utilities.py
# Gets information for gamflip using commandline tools
import subprocess

class GamflipUtilities():

    dev_list_output = ""
    started_ffmpeg = False
    ffmpeg = ""
    init_output = ""
    loopback_device = ""

    # Get list of potential cameras, filter out the loopback device
    def get_dev_list(self, combobox):
        # grab output of v4l2-ctl --list devices
        list_devices = subprocess.Popen(['v4l2-ctl', '--list-devices'], stdout=subprocess.PIPE)

        # pipe output of v4l2-ctl to grep and search for lines containing dev
        dev_loopback = subprocess.check_output(['grep', '/dev/'],stdin=list_devices.stdout)
        list_devices.wait()
        dev_loopback = dev_loopback.decode("utf-8").strip()

        # Only add device to the combobox if it's not the loopback device
        for device in dev_loopback.splitlines():
            if device.strip() != self.loopback_device:
                combobox.append_text(device.strip())
        return combobox

    # Get the loopback device
    def set_default_loopback(self, combobox):
        # grab output of v4l2-ctl --list devices
        list_devices = subprocess.Popen(['v4l2-ctl', '--list-devices'], stdout=subprocess.PIPE)

        # pipe output of v4l2-ctl into sed and grab the line after v4l2loopback
        loopback = subprocess.Popen(['sed', '-n', '/v4l2loopback/,+1p'],stdin=list_devices.stdout,stdout=subprocess.PIPE)

        # pipe ouput of sed into grep and look for devices
        dev_loopback = subprocess.check_output(['grep', '/dev/'],stdin=loopback.stdout)
        list_devices.wait()
        loopback.wait()

        # add the device that was returned
        self.loopback_device = dev_loopback.decode("utf-8").strip()
        combobox.append_text(self.loopback_device)
        return combobox

    # Apply filters
    def execute_filters(self, flip, grey, source, loopback):
        if self.started_ffmpeg:
            self.remove_filters()

        if flip and grey:
            self.ffmpeg = subprocess.Popen(['ffmpeg', '-f', 'v4l2', '-i', source, '-vf', 'eq=gamma=1.5:saturation=0,vflip', '-f', 'v4l2', loopback])
        else:
            if flip:
                self.ffmpeg = subprocess.Popen(['ffmpeg', '-f', 'v4l2', '-i', source, '-vf', 'vflip', '-f', 'v4l2', loopback])
            else:
                self.ffmpeg = subprocess.Popen(['ffmpeg', '-f', 'v4l2', '-i', source, '-vf', 'eq=gamma=1.5:saturation=0', '-f', 'v4l2', loopback])
        self.started_ffmpeg = True

    # Remove filters by terminating the ffmpeg process
    def remove_filters(self):
        self.ffmpeg.kill()
