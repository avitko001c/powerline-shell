import os
from powerline_shell.runcmd import Command
from powerline_shell.symbols import *
from powerline_shell.utils import ThreadedSegment, decode
from powerline_shell.color_compliment import stringToHashToColorAndOpposite, rgb2short
from powerline_shell.encoding import u

try:
    from shutil import wich  # Python-3.3 and later
except ImportError:
    which = lambda f: (lambda fp: os.path.exists(fp) and fp)(os.path.join('/usr/bin', f))


class Segment(ThreadedSegment):
    def run(self):
        self.logo = u(python.symbol)
        self.version = None
        try:
            if which('python'):
                self.cmd = Command(["python", "--version"])
                self.version = self.cmd.out.split()[1]
                FG, nil = stringToHashToColorAndOpposite(self.version)
                self.FG, self.nil = (rgb2short(*color) for color in [FG, nil])
                self.FG += 32
                self.BG = self.powerline.theme.PYTHON_VERSION_BG
        except OSError:
            self.version = None
        self.line = "{0} {1}".format(self.logo, self.version)

    def add_to_powerline(self):
        self.join()
        if not self.version:
            return
        self.powerline.append(self.line, self.FG, self.BG)
