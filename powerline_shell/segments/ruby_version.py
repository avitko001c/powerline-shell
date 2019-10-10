import os
from powerline_shell.symbols import *
from powerline_shell.utils import Command
from powerline_shell.colortrans import rgb2short
from powerline_shell.utils import ThreadedSegment, decode
from powerline_shell.color_compliment import stringToHashToColorAndOpposite, rgb2short
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding, u

try:
   from shutil import which  # Python-3.3 and later
except ImportError:
   from subprocess import check_output
   which = lambda x: check_output(['which', x]).decode('utf-8').strip('\n')


class Segment(ThreadedSegment):
    def run(self):
        self.logo = u(ruby.symbol)
        try:
            if which('ruby'):
                self.version = Command(["ruby", "-v"])).out.split()[1]
                try:
                    self.FG, self.BG = self.powerline.theme.RUBY_VERSION_FG, self.powerline.theme.RUBY_VERSION_BG
                except:
                    FG, BG = stringToHashToColorAndOpposite(self.version)
                    self.FG, self.BG = (rgb2short(*color) for color in [FG, BG])
                    self.FG += 32
        except OSError:
            self.version = None
        self.line = "{0} {1}".format(self.logo, self.version)

    def add_to_powerline(self):
        self.join()
        if not self.version:
            return
        self.powerline.append(self.line, self.FG, self.BG)
