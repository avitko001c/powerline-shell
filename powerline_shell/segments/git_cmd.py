import re
import os
import subprocess
from powerline_shell.symbols import *
from powerline_shell.utils import RepoStats, ThreadedSegment, get_git_subprocess_env
from powerline_shell.encoding import get_preferred_output_encoding


def parse_git_branch_info(status):
    info = re.search(
        '^## (?P<local>\S+?)''(\.{3}(?P<remote>\S+?)( \[(ahead (?P<ahead>\d+)(, )?)?(behind (?P<behind>\d+))?\])?)?$',
        status[0])
    return info.groupdict() if info else None


def _get_git_detached_branch():
    try:
        from git import Git
        git_cmd = lambda x: Git().describe(x)
    except:
        from powerline_shell.utils import Command
        git_cmd = lambda x: Command(['git', 'describe'] + x).text
    detached_ref = git_cmd(['--tags', '--always'])
    if detached_ref:
        branch = u'{} {}'.format(repostats_detatched(1), detached_ref)
    else:
        branch = 'Big Bang'
    return branch


def parse_git_stats(status):
    stats = RepoStats()
    for statusline in status[1:]:
        code = statusline[:2]
        if code == '??':
            stats.new += 1
        elif code in ('DD', 'AU', 'UD', 'UA', 'DU', 'AA', 'UU'):
            stats.conflicted += 1
        else:
            if code[1] != ' ':
                stats.changed += 1
            if code[0] != ' ':
                stats.staged += 1

    return stats


def build_stats():
    try:
        from git import Git
        git_status = Git(os.getcwd()).is_git_dir()
    except:
        git_status = False
        for p in os.getenv("PWD").split('/'):
            path += p + '/'
            path_list.append(path)
        for i in path_list:
            if os.path.isdir(i + ".git"):
                git_status = True
                break
            else:
                pass
    # Run thru getting stats unless we aren't in a git repo
    try:
        from git import Git
        git_cmd = lambda x: Git().status(x)
    except:
        from powerline_shell.utils import Command
        git_cmd = lambda x: Command(['git', 'status'] + x).text
    if git_status:
        try:
            pdata = git_cmd(['--porcelain', '-b'])
            p = subprocess.Popen(['git', 'status', '--porcelain', '-b'],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 env=get_git_subprocess_env())
        except:
            # Popen will throw an OSError if git is not found
            return None, None

        #pdata = p.communicate()

        status = pdata.splitlines()
        stats = parse_git_stats(status)
        branch_info = parse_git_branch_info(status)

        if branch_info:
            stats.ahead = branch_info['ahead']
            stats.behind = branch_info['behind']
            branch = branch_info['local']
        else:
            branch = _get_git_detached_branch()
        return stats, branch
    else:
        return None, None


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
            symbol = repostats_git()
        else:
            symbol = ""
        self.powerline.append(" " + symbol + self.branch + " ", fg, bg)
        self.stats.add_to_powerline(self.powerline)
