import os
import subprocess
from powerline_shell.utils import RepoStats, ThreadedSegment, get_git_subprocess_env
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding, u

try:
    from shutil import wich  # Python-3.3 and later
except ImportError:
    which = lambda f: (lambda fp: os.path.exists(fp) and fp)(os.path.join('/usr/bin', f))

def get_git_url():
    if which('git'):
        try:
            p = subprocess.Popen(['git', 'config', '--get', 'remote.origin.url'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=get_git_subprocess_env())
        except OSError:
            # Popen will throw an OSError if git is not found
            return 0
        pdata = p.communicate()
        if p.returncode != 0:
            return None
        return pdata[0].decode(get_preferred_output_encoding()).rstrip('\n')
    else:
        eventlog.info('git command not found: cannot use this segment')
        return 'None'


class Segment(ThreadedSegment):
    def run(self):
        self.git_url = get_git_url()
        self.logo = u(self.logos['git'])
        if 'bitbucket' in str(self.git_url):
            self.logo = u(self.logos['bitbucket'])
        elif 'github' in str(self.git_url):
            self.logo = u(self.logos['github'])

    def add_to_powerline(self):
        self.join()
        if not self.git_url:
            return

        bg = self.powerline.theme.GIT_URL_BG
        fg = self.powerline.theme.GIT_URL_FG

        sc = self.git_url if self.git_url != 'None' else ''
        url_str = u'{0} {1} {2}'.format(self.logo, sc, RepoStats.symbols['url'])
        self.powerline.append(url_str, fg, bg)
