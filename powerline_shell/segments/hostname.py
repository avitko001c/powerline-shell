from powerline_shell.utils import BasicSegment
from powerline_shell.color_compliment import stringToHashToColorAndOpposite
from powerline_shell.colortrans import rgb2short
from socket import gethostname


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        hostname = gethostname()
        FG, BG = stringToHashToColorAndOpposite(hostname)
        if powerline.segment_conf("hostname", "colorize"):
            # if we operate on a dark background then
            # we want the brighter color to always be the
            # background color
            FG, BG = (rgb2short(*color) for color in [FG, BG])
            host_prompt = " %s " % hostname.split(".")[0]
        if powerline.segment_conf("hostname", "dark") and sum(FG) > sum(BG):
            FG,BG = BG,FG
            FG, BG = (rgb2short(*color) for color in [FG, BG])
            host_prompt = " %s " % hostname.split(".")[0]
        else:
            if powerline.args.shell == "bash":
                host_prompt = r" \h "
            elif powerline.args.shell == "zsh":
                host_prompt = " %m "
            else:
                host_prompt = " %s " % gethostname().split(".")[0]
            FG, BG = powerline.theme.HOSTNAME_FG, powerline.theme.HOSTNAME_BG
        powerline.append(host_prompt, FG, BG)
