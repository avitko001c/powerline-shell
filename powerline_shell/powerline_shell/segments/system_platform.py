import platform
from powerline_shell.utils import BasicSegment
from powerline_shell.color_compliment import stringToHashToColorAndOpposite
from powerline_shell.colortrans import rgb2short

def get_cursor(version=None,prompt='\U0001F4BB '):
    if version == 'Darwin':
        prompt = ' \uf179'
    elif version == 'Linux':
        prompt = '\uf31a'
    elif version == 'Windows':
        prompt = '\ufab2'
    else:
        prompt = None
    return prompt

class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        system = platform.system()
        try:
            FG, BG = powerline.theme.PLATFORM_FG, powerline.theme.PLATFORM_BG
        except:
            FG, BG = stringToHashToColorAndOpposite(system)
            FG, BG = (rgb2short(*color) for color in [FG, BG])
        system_prompt = "{} ".format(get_cursor(system))
        if not system_prompt:
            return
        powerline.append(system_prompt, FG, BG)
