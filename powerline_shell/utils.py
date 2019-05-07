# -*- coding: utf-8 -*-

import sys
import os
import logging
from threading import Thread
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding

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
        'url': u'\uf959',
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
        from powerline_shell.brandicons import logos
        self.powerline = powerline
        self.segment_def = segment_def  # type: dict
        self.symbols = powerline.symbols
        self.logos = logos

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

    def get_brand_icon(self, brand, padding=None):
        if padding:
            self.padding = self.add_spaces_left(padding)
        self.icon = u(self.brands[brand] + self.padding if self.padding)

    def add_spaces_left(self, amount):
	    return (' ' * amount)


class BatteryStats(object):
    def __init__(self, Threshold):
        from powerline_shell.brandicons import Logo
        self.threshold = Threshold
        self.logos = logos


class ThreadedSegment(Thread, BasicSegment):
    def __init__(self, powerline, segment_def):
        super(ThreadedSegment, self).__init__()
        from powerline_shell.brandicons import logos
        self.powerline = powerline
        self.segment_def = segment_def  # type: dict
        self.symbols = powerline.symbols
        self.logos = logos


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
