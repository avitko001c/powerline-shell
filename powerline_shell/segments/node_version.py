import subprocess
from powerline_shell.utils import ThreadedSegment


class Segment(ThreadedSegment):
    def run(self):
        try:
            self.version = subprocess.check_output(['node', '--version']).decode('utf-8').rstrip()
        except OSError:
            self.version = None

    def add_to_powerline(self):
        self.join()
        if not self.version:
            return
        # FIXME no hard-coded colors
        self.powerline.append("node " + self.version, 15, 18)
