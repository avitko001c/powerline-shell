import subprocess
from powerline_shell.utils import RepoStats, ThreadedSegment, get_subprocess_env
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding


def _get_hg_branch():
    p = subprocess.Popen(["hg", "branch"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         env=get_subprocess_env())
    branch = p.communicate()[0].decode(get_preferred_output_encoding()).rstrip('\n')
    return branch


def parse_hg_stats(status):
    stats = RepoStats()
    for statusline in status:
        if statusline[0] == "A":
            stats.staged += 1
        elif statusline[0] == "?":
            stats.new += 1
        else:  # [M]odified, [R]emoved, (!)missing
            stats.changed += 1
    return stats


def _get_hg_status(output):
    """This function exists to enable mocking the `hg status` output in tests.
    """
    return output[0].decode(get_preferred_output_encoding()).splitlines()


def build_stats():
    # Check to see if we are in a git directory
    path = '/'
    for p in os.getenv("PWD").split('/'):
        path += p + '/'
        if os.path.isdir(path+'.git'):
            break
        else:
            return None, None
    try:
        p = subprocess.Popen(["hg", "status"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             env=get_subprocess_env())
    except OSError:
        # Will be thrown if hg cannot be found
        return None, None
    pdata = p.communicate()
    if p.returncode != 0:
        return None, None
    status = _get_hg_status(pdata)
    stats = parse_hg_stats(status)
    branch = _get_hg_branch()
    return stats, branch


class Segment(ThreadedSegment):
    def run(self):
        self.stats, self.branch = build_stats()

    def add_to_powerline(self):
        self.join()
        if not self.stats:
            return
        bg = self.powerline.theme.REPO_CLEAN_BG
        fg = self.powerline.theme.REPO_CLEAN_FG
        if self.stats.dirty:
            bg = self.powerline.theme.REPO_DIRTY_BG
            fg = self.powerline.theme.REPO_DIRTY_FG
        if self.powerline.segment_conf("vcs", "show_symbol"):
            symbol = RepoStats().symbols["hg"] + " "
        else:
            symbol = ""
        self.powerline.append(" " + symbol + self.branch + " ", fg, bg)
        self.stats.add_to_powerline(self.powerline)
