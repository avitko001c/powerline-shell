import subprocess
from powerline_shell.utils import BasicSegment
from powerline_shell.encoding import get_preferred_output_encoding, get_preferred_input_encoding

class Segment(BasicSegment):
    def add_to_powerline(self):
        try:
            kube_env = subprocess.check_output(['kubectl', 'config', 'current-context'], stderr=subprocess.STDOUT).decode(get_preferred_output_encoding()).rstrip()
        except:
            raise Exception('k8s: Not set')
            kube_env = None

        if kube_env:
            self.powerline.append(" %s " % str.strip(kube_env),
                             self.powerline.theme.KUBECONFIG_PATH_FG,
                             self.powerline.theme.KUBECONFIG_PATH_BG)
