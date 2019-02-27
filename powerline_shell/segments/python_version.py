import os
import subprocess
from powerline_shell.colortrans import rgb2short
from powerline_shell.utils import ThreadedSegment, decode
from powerline_shell.color_compliment import stringToHashToColorAndOpposite, rgb2short
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding

try:
    from shutil import wich  # Python-3.3 and later
except ImportError:
    which = lambda f: (lambda fp: os.path.exists(fp) and fp)(os.path.join('/usr/bin', f))


class Segment(ThreadedSegment):
    def add_to_powerline(self):
        try:
            if which('python'):
                output, version = decode(subprocess.check_output(["python", "--version"])).split()
                self.version = version
                FG, nil = stringToHashToColorAndOpposite(self.version)
                self.FG, self.nil = (rgb2short(*color) for color in [FG, nil])
                self.FG += 32
                self.BG = self.powerline.theme.PYTHON_VERSION_BG
        except OSError:
            self.version = None
        if not self.version:
            return
        self.powerline.append(" " + self.version + " ", self.FG, self.BG)
