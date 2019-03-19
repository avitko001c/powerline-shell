import os
import subprocess
from powerline_shell.color_compliment import stringToHashToColorAndOpposite
from powerline_shell.colortrans import rgb2short
from socket import gethostname
from powerline_shell.utils import ThreadedSegment, decode


output, version  = decode(subprocess.check_output(["python", "--version"], stderr=subprocess.STDOUT)).split()
ver = output.rstrip().lower()
hostname = gethostname()
FG, BG = stringToHashToColorAndOpposite(hostname)
FG, BG = (rgb2short(*color) for color in [FG, BG])
WFG, WBG = stringToHashToColorAndOpposite(version)
WFG, WBG = (rgb2short(*color) for color in [WFG, WBG])
print(FG, BG)
print(WFG, WBG)

symbols = {
    'detached': u'\u2693',
    'ahead': u'\u2B06',
    'behind': u'\u2B07',
    'staged': u'\u2714',
    'changed': u'\u270E',
    'new': u'?',
    'conflicted': u'\u273C',
    'stash': u'\u2398',
    'git': u'\uE0A0',
    'hg': u'\u263F',
    'bzr': u'\u2B61\u20DF',
    'fossil': u'\u2332',
    'svn': u'\u2446',
    'dot': u'●',
    'url': u'\uFF0A',
    'bigdot': u'\u2022',
    'web': u'\U0001F578',
}

for i in symbols:
    print(i, symbols[i])
print(version)
'''
⚫︎
MEDIUM BLACK CIRCLE
Unicode: U+26AB U+FE0E, UTF-8: E2 9A AB EF B8 8E

⚫︎
MEDIUM BLACK CIRCLE
Unicode: U+26AB U+FE0E, UTF-8: E2 9A AB EF B8 8E

＊
FULLWIDTH ASTERISK
Unicode: U+FF0A, UTF-8: EF BC 8A

'''
