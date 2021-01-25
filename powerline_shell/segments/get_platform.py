import platform
from powerline_shell.symbols import *
from powerline_shell.utils import BasicSegment


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
        FG = powerline.theme.PLATFORM_FG
        BG = powerline.theme.PLATFORM_BG
        if powerline.segment_conf("platform", "show_symbol"):
            system = platform.system()
            system_prompt = "%s " % get_cursor(system)
            powerline.append(system_prompt, FG, BG)
        else:
            if powerline.args.shell == "bash":
                host_prompt = r" \h "
            elif powerline.args.shell == "zsh":
                host_prompt = " %m "
            else:
                host_prompt = " %s " % get_cursor(platform.system())
            powerline.append(
                host_prompt, FG, BG
            )
