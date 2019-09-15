from powerline_shell.runcmd import Command
from git import Git
from ..utils import ThreadedSegment, warn


def get_vcs_dir():
    git = Git().is_git_dir()
    hg_return_code = Command(['hg', 'status'])
    svn_return_code = Command(['svn', 'info'])
    if git or hg_return_code.exitcode == 0 or svn_return_code.exitcode == 0:
        return True
    else:
        return False


class Segment(ThreadedSegment):
    def run(self):
        self.in_vcs_dir = get_vcs_dir()

    def add_to_powerline(self):
        self.join()
        if not self.in_vcs_dir:
            return
        if self.powerline.args.shell == "tcsh":
            warn("newline segment not supported for tcsh (yet?)")
            return
        self.powerline.append("\n",
                              self.powerline.theme.RESET,
                              self.powerline.theme.RESET,
                              separator=" ")
