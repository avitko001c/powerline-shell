# -*- coding: utf-8 -*-

import sys
import os
import logging
import traceback
import subprocess
import psutil
import public
from threading import Thread
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding

try:
   from shutil import which  # Python-3.3 and later
except ImportError:
   from subprocess import check_output
   which = lambda x: check_output(['which', x]).decode('utf-8').strip('\n')

py3 = sys.version_info[0] == 3

if py3:
    def unicode_(x):
        return str(x)


    def decode(x):
        return x.decode(get_preferred_output_encoding())
else:
    unicode_ = unicode
    decode = unicode


class RepoStats(object):
    symbols = {
        'detached': u'\u2693',
        'ahead': u'\u2B06',
        'behind': u'\u2B07',
        'staged': u'\u2714',
        'changed': u'\u270E',
        'new': u'\uf067',
        'conflicted': u'\u273C',
        'stash': u'\u2398',
        'git': u'\ue0a0',
        'git-name': u'\ue717',
        'hg': u'\u263F',
        'bzr': u'\u2B61\u20DF',
        'fossil': u'\u2332',
        'svn': u'\u2446',
        'url': u'\uf116',
    }

    def __init__(self, ahead=0, behind=0, new=0, changed=0, staged=0, conflicted=0):
        self.ahead = ahead
        self.behind = behind
        self.new = new
        self.changed = changed
        self.staged = staged
        self.conflicted = conflicted
        # print(self.symbols)

    def __eq__(self, other):
        return (
                self.ahead == other.ahead and
                self.behind == other.behind and
                self.new == other.new and
                self.changed == other.changed and
                self.staged == other.staged and
                self.conflicted == other.conflicted
        )

    @property
    def dirty(self):
        qualifiers = [
            self.new,
            self.changed,
            self.staged,
            self.conflicted,
        ]
        return sum(qualifiers) > 0

    def __getitem__(self, _key):
        return getattr(self, _key)

    def n_or_empty(self, _key):
        """Given a string name of one of the properties of this class, returns
        the value of the property as a string when the value is greater than
        1. When it is not greater than one, returns an empty string.

        As an example, if you want to show an icon for new files, but you only
        want a number to appear next to the icon when there are more than one
        new file, you can do:

            segment = repo_stats.n_or_empty("new") + icon_string
        """
        return unicode_(self[_key]) if int(self[_key]) > 1 else u''

    def add_to_powerline(self, powerline):
        def add(_key, fg, bg):
            if self[_key]:
                s = u" {}{} ".format(self.n_or_empty(_key), self.symbols[_key])
                powerline.append(s, fg, bg)

        color = powerline.theme
        add('ahead', color.GIT_AHEAD_FG, color.GIT_AHEAD_BG)
        add('behind', color.GIT_BEHIND_FG, color.GIT_BEHIND_BG)
        add('staged', color.GIT_STAGED_FG, color.GIT_STAGED_BG)
        add('changed', color.GIT_NOTSTAGED_FG, color.GIT_NOTSTAGED_BG)
        add('new', color.GIT_UNTRACKED_FG, color.GIT_UNTRACKED_BG)
        add('conflicted', color.GIT_CONFLICTED_FG, color.GIT_CONFLICTED_BG)


def set_logger(loglevel, logname):
    log_format = '%(asctime)s:%(levelname)s:%(message)s'
    formatter = logging.Formatter(log_format)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    if loglevel.lower() == "warning":
        level = logging.WARNING
    if loglevel.lower() == "critical":
        level = logging.CRITICAL
    if loglevel.lower() == "exception":
        level = logging.EXCEPTION
    if loglevel.lower() == "info":
        level = logging.INFO
    if loglevel.lower() == "debug":
        level = logging.DEBUG
    if loglevel.lower() == "error":
        level = logging.ERROR
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setLevel(level)
    stdout.setFormatter(formatter)

    logger = logging.Logger(logname)
    logger.setLevel(level)
    logger.addHandler(console)
    eventlog = EventLogger(logger, logname)
    return eventlog


def critical(msg):
    eventlog = set_logger("critical", 'powerline-shell')
    eventlog.critical('[powerline-shell] {0}', msg)


def exception(msg):
    eventlog = set_logger("exception", 'powerline-shell')
    eventlog.exception('[powerline-shell] {0}', msg)


def error(msg):
    eventlog = set_logger("error", 'powerline-shell')
    eventlog.error('[powerline-shell] {0}', msg)


def debug(msg):
    eventlog = set_logger("debug", 'powerline-shell')
    eventlog.debug('[powerline-shell] {0}', msg)


def info(msg):
    eventlog = set_logger("info", 'powerline-shell')
    eventlog.info('[powerline-shell] {0}', msg)


def warn(msg):
    eventlog = set_logger("warning", 'powerline-shell')
    eventlog.warn('[powerline-shell] {0}', msg)


class EventLogger(object):
    '''Proxy class for logging.Logger instance

    It emits messages in format ``{ext}:{prefix}:{message}`` where

    ``{ext}``
            is an EventLogger extension (e.g. “vim”, “shell”, “python”).
    ``{prefix}``
            is a local prefix, usually a segment name.
    ``{message}``
            is the original message passed to one of the logging methods.

    Each of the methods (``critical``, ``exception``, ``info``, ``error``,
    ``warn``, ``debug``) expects to receive message in an ``str.format`` format,
    not in printf-like format.

    Log is saved to the location :ref:`specified by user <config-common-log>`.
    '''

    def __init__(self, logger, ext):
        self.logger = logger
        self.ext = ext
        self.prefix = ''
        self.last_msgs = {}

    def _log(self, attr, msg, *args, **kwargs):
        from powerline_shell.unicode import safe_unicode
        prefix = kwargs.get('prefix') or self.prefix
        prefix = self.ext + ((':' + prefix) if prefix else '')
        msg = safe_unicode(msg)
        if args or kwargs:
            args = [safe_unicode(s) if isinstance(s, bytes) else s for s in args]
            kwargs = dict((
                (k, safe_unicode(v) if isinstance(v, bytes) else v)
                for k, v in kwargs.items()
            ))
            msg = msg.format(*args, **kwargs)
        msg = prefix + ':' + msg
        key = attr + ':' + prefix
        if msg != self.last_msgs.get(key):
            getattr(self.logger, attr)(msg)
            self.last_msgs[key] = msg

    def critical(self, msg, *args, **kwargs):
        self._log('critical', msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self._log('exception', msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log('info', msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._log('error', msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self._log('warning', msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._log('debug', msg, *args, **kwargs)


class BasicSegment(object):
    def __init__(self, powerline, segment_def):
        from powerline_shell import symbols
        self.powerline = powerline
        self.segment_def = segment_def  # type: dict
        self.symbols = powerline.symbols

    def start(self):
        pass

    def error(self, msg):
        eventlog = set_logger("error", self.segment_def["type"])
        eventlog.error('[{0}] {1}', self.segment_def["type"], msg)

    def debug(self, msg):
        eventlog = set_logger("debug", self.segment_def["type"])
        eventlog.debug('[{0}] {1}', self.segment_def["type"], msg)

    def info(self, msg):
        eventlog = set_logger("info", self.segment_def["type"])
        eventlog.info('[{0}] {1}', self.segment_def["type"], msg)

    def warn(self, msg):
        eventlog = set_logger("warning", self.segment_def["type"])
        eventlog.warn('[{0}] {1}', self.segment_def["type"], msg)

    def add_spaces_left(self, amount):
	    return (' ' * amount)


class BatteryStats(object):
    def __init__(self, Threshold):
        from powerline_shell import symbols
        self.threshold = Threshold


class ThreadedSegment(Thread, BasicSegment):
    def __init__(self, powerline, segment_def):
        from powerline_shell import symbols
        super(ThreadedSegment, self).__init__()
        self.powerline = powerline
        self.segment_def = segment_def  # type: dict


class CommandNotFound(OSError):
    ''' Raise when the command entered is not found '''


@public.add
class Command(object):
    """Command class"""
    custom_popen_kwargs = None
    __readme__ = ["exc", "args", "code", "out", "err", "pid", "kill", "ok", "running", "__bool__"]

    def __init__(self, _command, cwd=None, env=None, background=False, **popen_kwargs):
        if isinstance(_command, str):
            self.command = _command.split()
        elif isinstance(_command, list):
            self.command = _command
        self.code, self._out, self._err = None, "", ""
        self.env = env
        self.cwd = cwd
        self.background = background
        self.custom_popen_kwargs = dict(popen_kwargs)
        self.kwargs = self.popen_kwargs
        self.kwargs["cwd"] = cwd
        if self.env:
            self.kwargs["env"].update(env)
        if self.background:
            self.kwargs["stdout"] = open(os.devnull, 'wb')
            self.kwargs["stderr"] = open(os.devnull, 'wb')
        self.run

    @property
    def run(self):
        self.code, self._out, self._err = None, "", ""
	try:
            self.valid = which(self.command[0])
	except:
            self.valid = None
        if not self.valid:
            msg = "CommandNotFoundError: [Errno 2] Command not found: {}: args: {}".format(self.command[0], self.command[1:])
            raise CommandNotFound(msg)
        self.process = subprocess.Popen(self.command, **self.kwargs)
        self.process.args = self.command
        if not self.background:
            self._out, self._err = self.process.communicate()
            self.code = self.process.returncode
        self._args = self.process.args
        self._out = self._out.rstrip()
        self._err = self._err.rstrip()
        self._code = self.code
        self._pid = self.process.pid
        return self

    def __bool__(self):
        """return True if status code is 0"""
        return self.ok

    def __non_zero__(self):
        """return True if status code is 0"""
        return self.ok

    def __str__(self):
        return "<Process code=%s>" % self.code

    def exc(self):
        """raise OSError if status code is not 0. returns self"""
        if self.pid and not self.ok:
            output = self.err
            if not self.err:
                output = self.out
            if output:
                raise OSError("%s exited with code %s\n%s" % (self.args, self.code, output))
            raise OSError("%s exited with code %s" % (self.args, self.code))
        return self

    def _raise(self):
        """deprecated"""
        return self.exc()

    def kill(self, signal=None):
        """kill process. return error string if error occured"""
        if self.running:
            args = list(map(str, filter(None, ["kill", signal, self.pid])))
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            if "No such process" not in err.decode():
                return err.decode().rstrip()

    def rerun(self):
        self.run
        return self.out

    @property
    def pid(self):
        """return rocess pid"""
        return self._pid

    @property
    def args(self):
        """return arguments list"""
        return self._args

    @property
    def exitcode(self):
        """return status code"""
        return self._code

    @property
    def err(self):
        """return stderr string"""
        return self._err

    @property
    def out(self):
        """return stdout string"""
        if isinstance(self._out, list):
            return self._out
        try:
            if '\n' in self._out:
                return self._out.split('\n')
        except TypeError:
            return self._out
        return self._out.split()

    @property
    def text(self):
        """return stdout+stderr string"""
        return "\n".join(filter(None, self.out + [self.err])).replace('\n', ' ')

    @property
    def ok(self):
        """return True if status code is 0, else False"""
        return self.code == 0

    @property
    def running(self):
        """return True if process is running, else False"""
        try:
            os.kill(self.pid, 0)
            return psutil.Process(self.pid).status() != psutil.STATUS_ZOMBIE
        except OSError:
            return False
        except psutil._exceptions.NoSuchProcess:
            return False

    @property
    def popen_kwargs(self):
        kwargs = self._default_popen_kwargs
        kwargs.update(self.custom_popen_kwargs)
        return kwargs

    @property
    def _default_popen_kwargs(self):
        return {
            'env': os.environ.copy(),
            'stdin': subprocess.PIPE,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'shell': False,
            'universal_newlines': True,
            'bufsize': 0
        }


def import_file(module_name, path):
    # An implementation of https://stackoverflow.com/a/67692/683436
    if py3 and sys.version_info[1] >= 5:
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, path)
        if not spec:
            raise ImportError()
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    elif py3:
        from importlib.machinery import SourceFileLoader
        return SourceFileLoader(module_name, path).load_module()
    else:
        import imp
        return imp.load_source(module_name, path)


def get_PATH():
    """Normally gets the PATH from the OS. This function exists to enable
    easily mocking the PATH in tests.
    """
    return os.getenv("PATH")


def get_subprocess_env(**envs):
    defaults = {
        # https://github.com/milkbikis/powerline-shell/pull/153
        "PATH": get_PATH(),
    }
    defaults.update(envs)
    env = dict(os.environ)
    env.update(defaults)
    return env


def get_git_subprocess_env():
    # LANG is specified to ensure git always uses a language we are expecting.
    # Otherwise we may be unable to parse the output.
    return get_subprocess_env(LANG="C")
