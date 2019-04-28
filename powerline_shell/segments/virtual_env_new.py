import os
from powerline_shell.utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        env = os.getenv('VIRTUAL_ENV') \
              or os.getenv('CONDA_ENV_PATH') \
              or os.getenv('CONDA_DEFAULT_ENV' \
                           or os.getenv('POWERLINE_ENV_NAME'))
        if os.getenv('VIRTUAL_ENV') \
                and os.path.basename(env) == '.venv' and not os.getenv('POWERLINE_ENV_NAME'):
            env = os.path.basename(os.path.dirname(env))
        elif os.getenv('POWERLINE_ENV_NAME'):
            env = os.getenv('POWERLINE_ENV_NAME')
        if not env:
            return
        env_name = os.path.basename(env)
        bg = self.powerline.theme.VIRTUAL_ENV_BG
        fg = self.powerline.theme.VIRTUAL_ENV_FG
        self.powerline.append(" " + env_name + " ", fg, bg)
