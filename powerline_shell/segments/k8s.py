from powerline_shell.runcmd import Command
from powerline_shell.symbols import *
from powerline_shell.utils import ThreadedSegment, decode
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding, u
from shutil import which

class Segment(ThreadedSegment):
    def add_to_powerline(self):
        self.logo = u(kubernetes.symbol)
        self.kube_env = None
        if which('kubectl'):
            try:
                self.cmd = Command(['kubectl', 'config', 'current-context'])
                self.kube_env = self.cmd.out.rstrip()
            except:
                raise Exception('k8s: Not set')

        if not self.kube_env:
            return
        self.line = "{0} {1}".format(self.logo, self.kube_env)
        self.powerline.append( self.line,
                         self.powerline.theme.KUBECONFIG_PATH_FG,
                         self.powerline.theme.KUBECONFIG_PATH_BG)
