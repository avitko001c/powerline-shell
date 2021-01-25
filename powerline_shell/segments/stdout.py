from powerline_shell.utils import ThreadedSegment, Command


class Segment(ThreadedSegment):
    def run(self):
        cmd = self.segment_def["command"]
        self.output = Command(cmd).strip()
        # TODO handle OSError
        # TODO handle no command defined or malformed

    def add_to_powerline(self):
        self.join()
        self.powerline.append(
            " %s " % self.output,
            self.segment_def.get("fg_color", self.powerline.theme.PATH_FG),
            self.segment_def.get("bg_color", self.powerline.theme.PATH_BG))
