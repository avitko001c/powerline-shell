import subprocess
from powerline_shell.utils import ThreadedSegment
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding


class Segment(ThreadedSegment):
    def run(self):
        try:
            p1 = subprocess.Popen(["npm", "--version"], stdout=subprocess.PIPE)
            self.version = p1.communicate()[0].decode(get_preferred_output_encoding()).rstrip()
        except OSError:
            self.version = None

    def add_to_powerline(self):
        self.join()
        if self.version:
            # FIXME no hard-coded colors
            self.powerline.append("npm " + self.version, 15, 18)
