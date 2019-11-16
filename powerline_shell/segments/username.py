from powerline_shell.utils import BasicSegment
from powerline_shell.colortrans import rgb2short
from powerline_shell.color_compliment import stringToHashToColorAndOpposite
import os
import getpass


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        if powerline.args.shell == "bash":
            user_prompt = r" \u "
        elif powerline.args.shell == "zsh":
            user_prompt = " %n "
        else:
            user_prompt = " %s " % os.getenv("USER")

        fgcolor, bgcolor = stringToHashToColorAndOpposite(user_prompt)
        if getpass.getuser() == "root":
            bgcolor = powerline.theme.USERNAME_ROOT_BG
            fgcolor = powerline.theme.USERNAME_ROOT_FG
        if powerline.segment_conf("username", "dark") and sum(fgcolor) < sum(bgcolor):
            fgcolor, bgcolor = bgcolor, fgcolor
            fgcolor, bgcolor = (rgb2short(*color) for color in [fgcolor, bgcolor])
        else:
            fgcolor, bgcolor = powerline.theme.USERNAME_FG, powerline.theme.USERNAME_BG
        powerline.append(user_prompt, fgcolor, bgcolor)
