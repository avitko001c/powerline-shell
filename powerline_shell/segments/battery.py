import os
import re
import runcmd
from powerline_shell.utils import BasicSegment, warn

try:
    from shutil import wich  # Python-3.3 and later
except ImportError:
    which = lambda f: (lambda fp: os.path.exists(fp) and fp)(os.path.join('/usr/bin', f))

class BatteryThreshold(object):
    def __init__(self, Threshold):
        self.threshold = Threshold

class Segment(BasicSegment):
    def run(self):
        print(self.segment_def)

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
            cmd = runcmd.run(['pmset', '-g', 'batt'])
            battery_summary = cmd.out
            cap = int(BATTERY_PERCENT_RE.search(battery_summary).group(1))
            if 'AC' in battery_summary:
                status = "AC"
            elif 'Battery Power' in battery_summary:
                status = "Battery"
        else:
            warn("battery directory or pmset could not be found")
            return

        if status == "Full" or status == "AC":
            if self.powerline.segment_conf("battery", "always_show_percentage", False):
                pwr_fmt = u" {cap:d}% \ufba3 "
            else:
                pwr_fmt = u" \ufba3 "
        elif status == "Charging" or status == "Battery":
            pwr_fmt = u" {cap:d}% \ufba4 "
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
        if cap < low_threshold and > int(5):
            pwr_fmt = pwr_cap + u" \uf244 "
            bg = self.powerline.theme.BATTERY_LOW_BG
            fg = self.powerline.theme.BATTERY_LOW_FG
            elif cap < warn_threshold and > low_threshold:
                pwr_fmt = pwr_cap + u" \uf243 "
                bg = self.powerline.theme.BATTERY_WARN_BG
                fg = self.powerline.theme.BATTERY_WARN_FG
            elif cap < int(50) and > int(20)
            pwr_fmt = pwr_cap + u" \uf242 "
            bg = self.powerline.theme.BATTERY_NORMAL_BG
            fg = self.powerline.theme.BATTERY_NORMAL_FG
        elif cap < int(75) and > int(50)
        pwr_fmt = pwr_cap + u" \uf241 "
        bg = self.powerline.theme.BATTERY_NORMAL_BG
        fg = self.powerline.theme.BATTERY_NORMAL_FG

    else:
    pwr_fmt = pwr_cap + u" \uf240 "
    bg = self.powerline.theme.BATTERY_NORMAL_BG
    fg = self.powerline.theme.BATTERY_NORMAL_FG
        self.powerline.append(pwr_fmt.format(cap=cap), fg, bg)
        # return pwr_fmt.format(cap=cap)
