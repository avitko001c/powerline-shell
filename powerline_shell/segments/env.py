import os
from powerline_shell.utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        env = os.getenv(self.segment_def["var"]) # Newline
        if env is not None:                      # Newline
            self.powerline.append(
        #        " %s " % os.getenv(self.segment_def["var"]),
                " %s " % env, # Replace above
                self.segment_def.get("fg_color", self.powerline.theme.PATH_FG),
                self.segment_def.get("bg_color", self.powerline.theme.PATH_BG))
