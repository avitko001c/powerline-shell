import os
from powerline_shell.symbols import *
from powerline_shell.utils import RepoStats, ThreadedSegment, get_git_subprocess_env, Command
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding, u
try:
    from path import Path
except:
    from pathlib import Path
try:
   from shutil import which  # Python-3.3 and later
except ImportError:
   from subprocess import getoutput
   which = lambda x: getoutput(['which', x])
try:
    from git import Git, GitCommandError, GitCommandNotFound
    git_cmd = lambda x: Git().config(x)
except ImportError:
    git_executable = which('git')
    git_cmd = lambda x: Command([git_executable] + x).text

hg_executable = which('hg')
hg_cmd = lambda x: Command([hg_executable] + x).text

def check_git_dir():
    git_dir = Git(os.getcwd()).is_git_dir()
    try:
        hg_dir = Path(os.getcwd() + '/.hg').isdir()
    except:
        hg_dir = Path(os.getcwd() + '/.hg').is_dir()
    if git_dir:
        return git_dir
    if hg_dir:
        return hg_dir
    return False

def get_git_url():
    try:
        git_url = git_cmd(['--get', 'remote.origin.url'])
        return git_url
    except GitCommandError:
        try:
            git_url = hg_cmd(['config', 'paths.default'])
            return git_url
        except:
            return None
        return None

class Segment(ThreadedSegment):
    def __init__(self, powerline, seg_conf):
        super().__init__(powerline, seg_conf)
        self.git_url = get_git_url()

    def run(self):
        self.logo = u(git(1))
        if 'bitbucket' in str(self.git_url):
            self.logo = u(bitbucket(1))
        elif 'github' in str(self.git_url):
            self.logo = u(github(1))

    def add_to_powerline(self):
        self.join()
        if not self.git_url:
            return

        bg = self.powerline.theme.GIT_URL_BG
        fg = self.powerline.theme.GIT_URL_FG

        sc = self.git_url if self.git_url != 'None' else ''
        url_str = u'{0} {1} {2}'.format(self.logo, sc, RepoStats.symbols['url'])
        self.powerline.append(url_str, fg, bg)
