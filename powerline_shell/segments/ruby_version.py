import os
import subprocess
from powerline_shell.utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline

        try:
            p1 = subprocess.Popen(['ruby', '-v'], stdout=subprocess.PIPE)
            ruby_and_gemset = subprocess.check_output(['sed', "s/ (.*//"], stdin=p1.stdout).decode('utf-8').rstrip()

            gem_set = os.environ.get('GEM_HOME', '@').split('@')

            if len(gem_set) > 1:
                ruby_and_gemset += "@{}".format(gem_set.pop())

            powerline.append(ruby_and_gemset, 15, 1)
        except OSError:
            return
