from powerline_shell.utils import BasicSegment
from powerline_shell.encoding import u
from powerline_shell.symbols import *
import os


class Segment(BasicSegment):

    def add_to_powerline(self):
        self.logo = u(aws.pad(1))
        self.aws_region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        if self.aws_region:
            self.region = os.path.basename(self.aws_region)
            self.line = "{0} {1}".format(self.logo, self.region)
            self.powerline.append(self.line,
                                  self.powerline.theme.AWS_REGION_FG,
                                  self.powerline.theme.AWS_REGION_BG)
