from powerline_shell.utils import BasicSegment
import os


class Segment(BasicSegment):
    def add_to_powerline(self):
        aws_region = os.environ.get("AWS_REGION") or \
            os.environ.get("AWS_DEFAULT_REGION")
        if aws_region:
            self.powerline.append(" %s " % os.path.basename(aws_region),
                                  self.powerline.theme.AWS_REGION_FG,
                                  self.powerline.theme.AWS_REGION_BG)
