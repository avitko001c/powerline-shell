import os
import subprocess
from powerline_shell.utils import BasicSegment
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding


class Segment(BasicSegment):
    def add_to_powerline(self):
        bg = self.powerline.theme.RUBY_VERSION_BG
        fg = self.powerline.theme.RUBY_VERSION_FG
        powerline = self.powerline

        try:
            p1 = subprocess.Popen(['ruby', '-v'], stdout=subprocess.PIPE)
            ruby_and_gemset = subprocess.check_output(['sed', "s/ (.*//"], stdin=p1.stdout).decode(get_preferred_output_encoding()).rstrip()

            gem_set = os.environ.get('GEM_HOME', '@').split('@')

            if len(gem_set) > 1:
                ruby_and_gemset += "@{}".format(gem_set.pop())

            powerline.append(ruby_and_gemset, fg, bg)
        except OSError:
            return
