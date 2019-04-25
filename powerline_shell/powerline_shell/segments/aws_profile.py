import os
from powerline_shell.utils import BasicSegment
from powerline_shell.encoding import u


class Segment(BasicSegment):

    def add_to_powerline(self):
        self.logo = u(self.logos['aws'])
        self.aws_profile = os.environ.get("AWS_PROFILE") or os.environ.get("AWS_DEFAULT_PROFILE")
        if self.aws_profile:
            self.profile = os.path.basename(self.aws_profile)
            self.line = "{0}  {1}".format(self.logo, self.profile)
            self.powerline.append( self.line,
                                  self.powerline.theme.AWS_PROFILE_FG,
                                  self.powerline.theme.AWS_PROFILE_BG)
