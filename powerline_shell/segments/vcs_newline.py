import os
from powerline_shell.utils import Command
from git import Git
from powerline_shell.utils import ThreadedSegment, warn


def get_vcs_dir():
    git = Git(os.getcwd()).is_git_dir()
    try:
        hg_return_code = Command(['hg', 'status']).exitcode
    except:
        hg_return_code = 1
    try:
        svn_return_code = Command(['svn', 'info']).exitcode
    except:
        svn_return_code = 1
    if git or hg_return_code == 0 or svn_return_code == 0:
        return True
    else:
        return False


class Segment(ThreadedSegment):
    def add_to_powerline(self):
        self.join()
        self.in_vcs_dir = get_vcs_dir()
        if not self.in_vcs_dir:
            return
        if self.powerline.args.shell == "tcsh":
            warn("newline segment not supported for tcsh (yet?)")
            return
        self.powerline.append("\n",
                              self.powerline.theme.RESET,
                              self.powerline.theme.RESET,
                              separator="")
