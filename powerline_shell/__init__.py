#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import os
import sys
import json
import logging
import argparse
import importlib
from powerline_shell.utils import warn, py3, import_file
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding


def _current_dir():
    """Returns the full current working directory as the user would have used
    in their shell (ie. without following symbolic links).

    With the introduction of Bash for Windows, we can't use the PWD environment
    variable very easily. `os.sep` for windows is `\` but the PWD variable will
    use `/`. So just always use the `os` functions for dealing with paths. This
    also is fine because the use of PWD below is done to avoid following
    symlinks, which Windows doesn't have.

    For non-Windows systems, prefer the PWD environment variable. Python's
    `os.getcwd` function follows symbolic links, which is undesirable."""
    if os.name == "nt":
        return os.getcwd()
    return os.getenv("PWD") or os.getcwd()


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
    logger.addHandler(stdout)
    logger.addHandler(console)
    eventlog = EventLogger(logger, logname)
    return(eventlog)

def get_valid_cwd():
    """Determine and check the current working directory for validity.

    Typically, an directory arises when you checkout a different branch on git
    that doesn't have this directory. When an invalid directory is found, a
    warning is printed to the screen, but the directory is still returned
    as-is, since this is what the shell considers to be the cwd."""
    try:
        cwd = _current_dir()
    except:
        warn("Your current directory is invalid. If you open a ticket at " +
            "https://github.com/milkbikis/powerline-shell/issues/new " +
            "we would love to help fix the issue.")
        sys.stdout.write("> ")
        sys.exit(1)

    parts = cwd.split(os.sep)
    up = cwd
    while parts and not os.path.exists(up):
        parts.pop()
        up = os.sep.join(parts)
    if cwd != up:
        warn("Your current directory is invalid. Lowest valid directory: "
             + up)
    return cwd

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

class Powerline(object):
    symbols = {
        'compatible': {
            'lock': 'RO',
            'network': 'SSH',
            'separator': u'\u25B6',
            'separator_thin': u'\u276F'
        },
        'patched': {
            'lock': u'\uE0A2',
            'network': 'SSH',
            'separator': u'\uE0B0',
            'separator_thin': u'\uE0B1'
        },
        'flat': {
            'lock': u'\uE0A2',
            'network': 'SSH',
            'separator': '',
            'separator_thin': ''
        },
    }

    color_templates = {
        'bash': r'\[\e%s\]',
        'tcsh': r'%%{\e%s%%}',
        'zsh': '%%{%s%%}',
        'bare': '%s',
    }

    def __init__(self, args, config, theme):
        self.args = args
        self.config = config
        self.theme = theme
        self.cwd = get_valid_cwd()
        mode = config.get("mode", "patched")
        self.color_template = self.color_templates[args.shell]
        self.reset = self.color_template % '[0m'
        self.lock = Powerline.symbols[mode]['lock']
        self.network = Powerline.symbols[mode]['network']
        self.separator = Powerline.symbols[mode]['separator']
        self.separator_thin = Powerline.symbols[mode]['separator_thin']
        self.segments = []

    def segment_conf(self, seg_name, key, default=None):
        return self.config.get(seg_name, {}).get(key, default)

    def color(self, prefix, code):
        if code is None:
            return ''
        elif code == self.theme.RESET:
            return self.reset
        else:
            return self.color_template % ('[%s;5;%sm' % (prefix, code))

    def fgcolor(self, code):
        return self.color('38', code)

    def bgcolor(self, code):
        return self.color('48', code)

    def append(self, content, fg, bg, separator=None, separator_fg=None, sanitize=True):
        if self.args.shell == "bash" and sanitize:
            content = re.sub(r"([`$])", r"\\\1", content)
        self.segments.append((content, fg, bg,
            separator if separator is not None else self.separator,
            separator_fg if separator_fg is not None else bg))

    def draw(self):
        text = (''.join(self.draw_segment(i) for i in range(len(self.segments)))
                + self.reset) + ' '
        if py3:
            return text
        else:
            return text.encode(get_preferred_output_encoding())

    def draw_segment(self, idx):
        segment = self.segments[idx]
        next_segment = self.segments[idx + 1] if idx < len(self.segments)-1 else None

        return ''.join((
            self.fgcolor(segment[1]),
            self.bgcolor(segment[2]),
            segment[0],
            self.bgcolor(next_segment[2]) if next_segment else self.reset,
            self.fgcolor(segment[4]),
            segment[3]))


def find_config():
    for location in [
        "powerline-shell.json",
        "~/.powerline-shell.json",
        os.path.join(os.environ.get("XDG_CONFIG_HOME", "~/.config"), "powerline-shell", "config.json"),
    ]:
        full = os.path.expanduser(location)
        if os.path.exists(full):
            return full

DEFAULT_CONFIG = {
    "segments": [
        'virtual_env',
        'username',
        'hostname',
        'ssh',
        'cwd',
        'git',
        'hg',
        'jobs',
        'root',
    ]
}


class ModuleNotFoundException(Exception):
    pass


class CustomImporter(object):
    def __init__(self):
        self.file_import_count = 0

    def import_(self, module_prefix, module_or_file, description):
        try:
            mod = importlib.import_module(module_prefix + module_or_file)
        except ImportError:
            try:
                module_name = "_custom_mod_{0}".format(self.file_import_count)
                mod = import_file(module_name, os.path.expanduser(module_or_file))
                self.file_import_count += 1
            except (ImportError, IOError):
                msg = "{0} {1} cannot be found".format(description, module_or_file)
                raise ModuleNotFoundException( msg)
        return mod


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--generate-config', action='store_true',
                            help='Generate the default config and print it to stdout')
    arg_parser.add_argument('--shell', action='store', default='bash',
                            help='Set this to your shell type',
                            choices=['bash', 'tcsh', 'zsh', 'bare'])
    arg_parser.add_argument('--config', '-c', action='store',
                            help='Configuration file to load')
    arg_parser.add_argument('--loglevel', '-l', action='store',
                            help='set the loglevel you want: Default info')
    arg_parser.add_argument('prev_error', nargs='?', type=int, default=0,
                            help='Error code returned by the last command')
    args = arg_parser.parse_args()

    if args.loglevel:
        eventlog = set_logger(args.loglevel, 'powerline-shell')
    elif not args.loglevel:
        eventlog = set_logger('info', 'powerline-shell')

    if args.generate_config:
        eventlog.info(json.dumps(DEFAULT_CONFIG, indent=2))
        return 0

    if args.config and not os.path.exists(os.path.expanduser(args.config)):
        eventlog.info('Cannot find config file using default config file: {0}', args.config)
        config_path = find_config()
    elif args.config and os.path.exists(os.path.expanduser(args.config)):
        config_path = args.config
    else:
        config_path = find_config()
    if config_path:
        with open(config_path) as f:
            try:
                config = json.loads(f.read())
            except Exception as e:
                warn("Config file ({0}) could not be decoded! Error: {1}"
                     .format(config_path, e))
                config = DEFAULT_CONFIG
    else:
        config = DEFAULT_CONFIG

    custom_importer = CustomImporter()
    theme_mod = custom_importer.import_(
        "powerline_shell.themes.",
        config.get("theme", "default"),
        "Theme")
    theme = getattr(theme_mod, "Color")

    powerline = Powerline(args, config, theme)
    segments = []
    for seg_conf in config["segments"]:
        if not isinstance(seg_conf, dict):
            seg_conf = {"type": seg_conf}
        seg_name = seg_conf["type"]
        seg_mod = custom_importer.import_(
            "powerline_shell.segments.",
            seg_name,
            "Segment")
        segment = getattr(seg_mod, "Segment")(powerline, seg_conf)
        segment.start()
        segments.append(segment)
    for segment in segments:
        segment.add_to_powerline()
    sys.stdout.write(powerline.draw())
    return 0
