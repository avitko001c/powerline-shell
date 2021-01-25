from powerline_shell.utils import Command
from powerline_shell.symbols import *
from powerline_shell.utils import ThreadedSegment, decode
from powerline_shell.encoding import u


class Segment(ThreadedSegment):
    def run(self):
        self.version = None
        try:
            output = Command(['php', '-r', 'echo PHP_VERSION;'])
            self.version = output.out.split('-')[0] if '-' in output else output
            self.logo = u(php.symbol)
        except OSError:
            self.version = None

    def add_to_powerline(self):
        self.join()
        if not self.version:
            return
        # FIXME no hard-coded colors
        self.powerline.append(self.logo + self.version + " ", 15, 4)
