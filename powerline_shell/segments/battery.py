import os
import re
from powerline_shell.utils import BasicSegment, warn, Command
from powerline_shell.symbols import *
from powerline_shell.encoding import u

try:
    from shutil import which  # Python-3.3 and later
except ImportError:
    from subprocess import getoutput
    which = lambda f: getoutput('which {cmd}'.format(cmd=x))


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
            cmd = Command(['pmset', '-g', 'batt'])
            battery_summary = cmd.out
            for raw in battery_summary:
                line = raw.strip()
                if "Now drawing from" in line:
                    status = "Battery" if "'Battery Power'" in line else \
                        ('AC' if "'AC Power'" in line else "")
                elif "InternalBattery" in line:
                    m = re.search('([0-9]{1,3})%;', battery_summary[1])
                    if m is not None:
                        raw_cap = int(m.group(1))
                        cap = raw_cap if (0<=raw_cap and raw_cap <=100) else -1
                    m = re.search('[0-9]{1,3}%; ([a-zA-Z ]+);', battery_summary[1])
                    if m is not None:
                        source = m.group(1).strip()
                    break
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
            pwr_fmt = u" {cap:d}% "

        low_threshold = self.powerline.segment_conf("battery", "low_threshold", 10)
        warn_threshold =  self.powerline.segment_conf("battery", "warn_threshold", 20)
        bg = self.powerline.theme.BATTERY_NORMAL_BG
        fg = self.powerline.theme.BATTERY_NORMAL_FG
        if source == 'discharging':
            if cap <= low_threshold:
                pwr_fmt = str(' ') + str(cap) + u(battery_ten(1))
                bg = self.powerline.theme.BATTERY_LOW_BG
                fg = self.powerline.theme.BATTERY_LOW_FG
            elif cap > low_threshold and cap <= warn_threshold:
                pwr_fmt = str(' ') + str(cap) + u(battery_twenty(1))
                bg = self.powerline.theme.BATTERY_WARN_BG
                fg = self.powerline.theme.BATTERY_WARN_FG
            elif cap > warn_threshold and cap <= int(30):
                pwr_fmt = str(' ') + str(cap) + u(battery_thirty(1))
                bg = self.powerline.theme.BATTERY_NORMAL_BG
                fg = self.powerline.theme.BATTERY_NORMAL_FG
            elif cap > int(30) and cap <= int(40):
                pwr_fmt = str(' ') + str(cap) + u(battery_forty(1))
                bg = self.powerline.theme.BATTERY_NORMAL_BG
                fg = self.powerline.theme.BATTERY_NORMAL_FG
            elif cap > int(40) and cap <= int(50):
                pwr_fmt = str(' ') + str(cap) + u(battery_fifty(1))
                bg = self.powerline.theme.BATTERY_NORMAL_BG
                fg = self.powerline.theme.BATTERY_NORMAL_FG
            elif cap > int(50) and cap <= int(60):
                pwr_fmt = str(' ') + str(cap) + u(battery_sixty(1))
                bg = self.powerline.theme.BATTERY_NORMAL_BG
                fg = self.powerline.theme.BATTERY_NORMAL_FG
            elif cap > int(50) and cap <= int(70):
                pwr_fmt = str(' ') + str(cap) + u(battery_seventy(1))
                bg = self.powerline.theme.BATTERY_NORMAL_BG
                fg = self.powerline.theme.BATTERY_NORMAL_FG
            elif cap > int(70) and cap <= int(80):
                pwr_fmt = str(' ') + str(cap) + u(battery_seventy(1))
                bg = self.powerline.theme.BATTERY_NORMAL_BG
                fg = self.powerline.theme.BATTERY_NORMAL_FG
            elif cap > int(80) and cap <= int(90):
                pwr_fmt = str(' ') + str(cap) + u(battery_ninety(1))
                bg = self.powerline.theme.BATTERY_NORMAL_BG
                fg = self.powerline.theme.BATTERY_NORMAL_FG
            elif cap > int(90) and cap <= int(100):
                pwr_fmt = str(' ') + str(cap) + u(battery_hundred(1))
                bg = self.powerline.theme.BATTERY_NORMAL_BG
                fg = self.powerline.theme.BATTERY_NORMAL_FG
        elif source == "charging" or source == "charged":
            pwr_fmt = u(plug(1))
            bg = self.powerline.theme.BATTERY_NORMAL_BG
            fg = self.powerline.theme.BATTERY_NORMAL_FG
        elif not isinstance(cap, int):
            pwr_fmt = str(' ') + str(cap) + u(battery_error(1))
            bg = self.powerline.theme.BATTERY_LOW_BG
            fg = self.powerline.theme.BATTERY_LOW_FG
           

        self.powerline.append(pwr_fmt.format(cap=cap), fg, bg)
