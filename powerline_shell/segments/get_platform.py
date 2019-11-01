import platform
from powerline_shell.symbols import *
from powerline_shell.utils import BasicSegment
from powerline_shell.color_compliment import stringToHashToColorAndOpposite
from powerline_shell.colortrans import rgb2short


def get_cursor(version=None, prompt=laptop()):
    if version == "Darwin":
        prompt = apple()
    elif version == "Linux":
        prompt = linux()
    elif version == "Windows":
        prompt = windows()
    elif not version:
        prompt = prompt

    return prompt


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        if powerline.segment_conf("platform", "colorize"):
            system = platform.system()
            FG, BG = stringToHashToColorAndOpposite(system)
            FG, BG = (rgb2short(*color) for color in [FG, BG])
            system_prompt = "%s " % get_cursor(system)
            print(system_prompt)
            powerline.append(system_prompt, FG, BG)
        else:
            if powerline.args.shell == "bash":
                host_prompt = r" \h "
            elif powerline.args.shell == "zsh":
                host_prompt = " %m "
            else:
                host_prompt = " %s " % get_cursor(platform.system())
            powerline.append(
                host_prompt, powerline.theme.PLATFORM_FG, powerline.theme.PLATFORM_BG
            )
