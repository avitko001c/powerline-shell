import os
import re
import platform
import powerline_shell.runcmd as runcmd
from powerline_shell.utils import ThreadedSegment
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding


class Segment(ThreadedSegment):
    def run(self):
        self.num_jobs = 0
        if platform.system().startswith('CYGWIN'):
            # cygwin ps is a special snowflake...
            output_proc = runcmd.run(['ps', '-af'])
            output = list(map(lambda l: int(l.split()[2].strip()),
                              output_proc.out.splitlines()[1:]))
            self.num_jobs = output.count(os.getppid()) - 1
        else:
            pppid_proc = runcmd.run(['ps', '-p', str(os.getppid()), '-oppid='])
            pppid = pppid_proc.out.strip()
            output_proc = runcmd.run(['ps', '-a', '-o', 'ppid'])
            output = output_proc.out
            self.num_jobs = len(re.findall(str(pppid), output)) - 1

    def add_to_powerline(self):
        self.join()
        if self.num_jobs > 0:
            self.powerline.append(' %d ' % self.num_jobs,
                                  self.powerline.theme.JOBS_FG,
                                  self.powerline.theme.JOBS_BG)
