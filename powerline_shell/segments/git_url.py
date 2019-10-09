import os
from powerline_shell.symbols import *
from powerline_shell.utils import RepoStats, ThreadedSegment, get_git_subprocess_env, Command
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding, u
try:
   from shutil import which  # Python-3.3 and later
except ImportError:
   from subprocess import check_output
   which = lambda x: check_output(['which', x]).decode('utf-8').strip('\n')
try:
    from git import Git
    git = lambda x: Git(['git'] + x)
except ImportError:
    git_executable = which('git')
    git = lambda x: Command([git_executable] + x).text()

def check_git_dir():
    git_dir = Git(os.getcwd()).is_git_dir()
    if git_dir:
        return True
    return False

def get_git_url():
    git_url = git(['config', '--get', 'remote.origin.url'])
    if not git_url:
        return None

class Segment(ThreadedSegment):
    def run(self):
        self.git_url = get_git_url()
        self.logo = u(git.dump())
        if 'bitbucket' in str(self.git_url):
            self.logo = u(bitbucket.dump())
        elif 'github' in str(self.git_url):
            self.logo = u(github.dump())

    def add_to_powerline(self):
        self.join()
        if not self.git_url:
            return

        bg = self.powerline.theme.GIT_URL_BG
        fg = self.powerline.theme.GIT_URL_FG

        sc = self.git_url if self.git_url != 'None' else ''
        url_str = u'{0} {1} {2}'.format(self.logo, sc, RepoStats.symbols['url'])
        self.powerline.append(url_str, fg, bg)
