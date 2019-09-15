#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import psutil
import public


@public.add
class Command(object):
    """Command class"""
    custom_popen_kwargs = None
    __readme__ = ["exc", "args", "code", "out", "err", "pid", "kill", "ok", "running", "__bool__"]

    def __init__(self, _command, cwd=None, env=None, background=False, **popen_kwargs):
        code, out, err = None, "", ""
        self.custom_popen_kwargs = dict(popen_kwargs)
        if isinstance(_command, str):
            self.command = _command.split()
        elif isinstance(_command, list):
            self.command = _command
        kwargs = self.popen_kwargs
        kwargs["cwd"] = cwd
        if env:
            kwargs["env"].update(env)
        if background:
            kwargs["stdout"] = open(os.devnull, 'wb')
            kwargs["stderr"] = open(os.devnull, 'wb')
        self.process = subprocess.Popen(self.command, **kwargs)
        """Popen.args python3 only"""
        self.process.args = _command
        if not background:
            out, err = self.process.communicate()
            code = self.process.returncode
        self._args = self.process.args
        self._out = out.rstrip()
        self._err = err.rstrip()
        self._code = code
        self._pid = self.process.pid

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
        return self._out

    @property
    def text(self):
        """return stdout+stderr string"""
        return "\n".join(filter(None, [self.out, self.err]))

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

