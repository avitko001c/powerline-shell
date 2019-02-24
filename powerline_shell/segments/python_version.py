import os
import subprocess
from powerline_shell.utils import ThreadedSegment, decode
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding

try:
    from shutil import wich  # Python-3.3 and later
except ImportError:
    which = lambda f: (lambda fp: os.path.exists(fp) and fp)(os.path.join('/usr/bin', f))


class Segment(ThreadedSegment):
    def add_to_powerline(self):
        try:
            if which('python'):
                output, version = decode(subprocess.check_output(["python", "--version"], stderr=subprocess.STDOUT)).split()
                self.version = version
        except OSError:
            self.version = None
        if not self.version:
            return
        # FIXME no hard-coded colors
        self.powerline.append(" " + self.version + " ", 15, 24)
