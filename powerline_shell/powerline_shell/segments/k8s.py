import subprocess
from powerline_shell.utils import ThreadedSegment, decode
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding, u
from shutil import which

class Segment(ThreadedSegment):
    def add_to_powerline(self):
        self.logo = u(self.logos['kubernetes'])
        kube_env = None
        if which('kubectl'):
            try:
                kube_env = decode(subprocess.check_output(['kubectl', 'config', 'current-context'], stderr=subprocess.STDOUT)).rstrip()
            except:
                raise Exception('k8s: Not set')

        if not kube_env:
            return
        self.line = "{0} {1}".format(self.logo, kube_env)
        self.powerline.append( self.line,
                         self.powerline.theme.KUBECONFIG_PATH_FG,
                         self.powerline.theme.KUBECONFIG_PATH_BG)
