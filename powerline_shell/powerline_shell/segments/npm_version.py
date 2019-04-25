import subprocess
from powerline_shell.utils import ThreadedSegment
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding


class Segment(ThreadedSegment):
    def add_to_powerline(self):
        try:
            self.version = subprocess.check_output(["npm", "--version"],).decode(get_preferred_output_encoding()).rstrip()
            #self.version = p1.communicate()[0].decode(get_preferred_output_encoding()).rstrip()
        except OSError:
            self.version = None

        if self.version:
            # FIXME no hard-coded colors
            self.powerline.append("npm " + self.version, 15, 18)
