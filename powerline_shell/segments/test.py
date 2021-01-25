import os
import subprocess
from powerline_shell.utils import BasicSegment
from powerline_shell.color_compliment import stringToHashToColorAndOpposite, rgb2short
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding
try:
    from shutil import wich  # Python-3.3 and later
except ImportError:
    which = lambda f: (lambda fp: os.path.exists(fp) and fp)(os.path.join('/usr/bin', f))


class Segment(BasicSegment):
    def run(self):
        self.logo = '\ue791 '
        self.prompt = None
        if which('ruby'):
            try:
                output = subprocess.check_output(['ruby', '-v'], stderr=subprocess.STDOUT).decode(get_preferred_output_encoding())
                self.version = output.split(' ')[1]
                self.prompt = " {}{} ".format(self.logo, self.version)
            except OSError:
                self.prompt = None

    def add_to_powerline(self):
        self.join()
        powerline = self.powerline
        if not self.prompt:
            return None
        try:
            FG, BG = self.powerline.theme.RUBY_VERSION_BG, self.powerline.theme.RUBY_VERSION_FG
        except:
            FG, BG = stringToHashToColorAndOpposite(self.version)
            FG, BG = (rgb2short(*color) for color in [FG, BG])
        print(self.prompt)
        powerline.append(self.prompt, FG, BG)
