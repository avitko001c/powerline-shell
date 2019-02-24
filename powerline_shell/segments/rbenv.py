import subprocess
from powerline_shell.utils import BasicSegment
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        try:
            p1 = subprocess.Popen(["rbenv", "local"], stdout=subprocess.PIPE)
            version = p1.communicate()[0].decode(get_preferred_output_encoding()).rstrip()
            if len(version) <= 0:
                    return
            powerline.append(' %s ' % version,
                             powerline.theme.VIRTUAL_ENV_FG,
                             powerline.theme.VIRTUAL_ENV_BG)
        except OSError:
            return
