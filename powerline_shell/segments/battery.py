import os
import re
import subprocess 
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding
from powerline_shell.utils import BasicSegment, warn

try:
    from shutil import wich  # Python-3.3 and later
except ImportError:
    which = lambda f: (lambda fp: os.path.exists(fp) and fp)(os.path.join('/usr/bin', f))

class Segment(BasicSegment):

    def add_to_powerline(self):
        ''' See discussion in https://github.com/banga/powerline-shell/pull/204
            regarding the directory where battery info is saved
        '''
        if os.path.exists("/sys/class/power_supply/BAT0"):
            dir_ = "/sys/class/power_supply/BAT0"
            with open(os.path.join(dir_, "capacity")) as f:
                cap = int(f.read().strip())
            with open(os.path.join(dir_, "status")) as f:
                status = f.read().strip()
        elif os.path.exists("/sys/class/power_supply/BAT1"):
            dir_ = "/sys/class/power_supply/BAT1"
            with open(os.path.join(dir_, "capacity")) as f:
                cap = int(f.read().strip())
            with open(os.path.join(dir_, "status")) as f:
                status = f.read().strip()
        elif which('pmset'):
            BATTERY_PERCENT_RE = re.compile(r'(\d+)%')
            battery_summary = subprocess.check_output(['pmset', '-g', 'batt']).decode(get_preferred_output_encoding())
            #battery_cmd = subprocess.Popen(['pmset', '-g', 'batt'], stdout=subprocess.PIPE)
            #battery_summary = battery_cmd.communicate()[0].decode(get_preferred_output_encoding()).rstrip()
            cap = int(BATTERY_PERCENT_RE.search(battery_summary).group(1))
            #cap = "".join([battery_percent,"%"])
            if 'AC' in battery_summary:
                status = "AC"
            elif 'Battery Power' in battery_summary:
                status = "Battery"
        else:
            warn("battery directory or pmset could not be found")
            return

        if status == "Full" or status == "AC":
            if self.powerline.segment_conf("battery", "always_show_percentage", False):
                pwr_fmt = u" {cap:d}% \U0001F50C "
            else:
                pwr_fmt = u" \U0001F50C "
        elif status == "Charging" or status == "Battery":
            pwr_fmt = u" {cap:d}% \u26A1 "
        else:
            pwr_fmt = " {cap:d}% "

        if cap < self.powerline.segment_conf("battery", "low_threshold", 10):
            bg = self.powerline.theme.BATTERY_LOW_BG
            fg = self.powerline.theme.BATTERY_LOW_FG
        elif cap < self.powerline.segment_conf("battery", "warn_threshold", 20):
            bg = self.powerline.theme.BATTERY_WARN_BG
            fg = self.powerline.theme.BATTERY_WARN_FG
        else:
            bg = self.powerline.theme.BATTERY_NORMAL_BG
            fg = self.powerline.theme.BATTERY_NORMAL_FG
        self.powerline.append(pwr_fmt.format(cap=cap), fg, bg)
