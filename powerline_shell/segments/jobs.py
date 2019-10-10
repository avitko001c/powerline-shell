import os
import re
import platform
from powerline_shell.utils import Command
from powerline_shell.utils import ThreadedSegment
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding


class Segment(ThreadedSegment):
    def run(self):
        self.num_jobs = 0
        if platform.system().startswith('CYGWIN'):
            # cygwin ps is a special snowflake...
            output_proc = Command(['ps', '-af'])
            output = list(map(lambda l: int(l.split()[2].strip()),
                              output_proc.text.splitlines()[1:]))
            self.num_jobs = output.count(os.getppid()) - 1
        else:
            pppid_proc = Command(['ps', '-p', str(os.getppid()), '-oppid='])
            pppid = pppid_proc.out
            output_proc = Command(['ps', '-a', '-o', 'ppid'])
            output = output_proc.text
            self.num_jobs = len(re.findall(str(pppid), output)) - 1

    def add_to_powerline(self):
        self.join()
        if self.num_jobs > 0:
            self.powerline.append(' %d ' % self.num_jobs,
                                  self.powerline.theme.JOBS_FG,
                                  self.powerline.theme.JOBS_BG)
