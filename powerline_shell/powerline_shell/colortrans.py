#! /usr/bin/env python

"""
Code is modified (fairly heavily) by hryanjones@gmail.com from
https://gist.github.com/MicahElliott/719710

Convert values between RGB tuples and xterm-256 color codes.

Nice long listing of all 256 colors and their codes. Useful for
developing console color themes, or even script output schemes.

Resources:
* http://en.wikipedia.org/wiki/8-bit_color
* http://en.wikipedia.org/wiki/ANSI_escape_code
* /usr/share/X11/rgb.txt

I'm not sure where this script was inspired from. I think I must have
written it from scratch, though it's been several years now.
"""

__author__    = 'Micah Elliott http://MicahElliott.com'
__version__   = '0.1'
__copyright__ = 'Copyright (C) 2011 Micah Elliott.  All rights reserved.'
__license__   = 'WTFPL http://sam.zoy.org/wtfpl/'

#---------------------------------------------------------------------


def hexstr2num(hexstr):
    return int(hexstr, 16)

def rgbstring2tuple(s):
    return tuple([hexstr2num(h) for h in (s[:2], s[2:4], s[4:])])

RGB2SHORT_DICT = {
    (0, 0, 0):     16,
    (0, 0, 95):    17,
    (0, 0, 128):   4,
    (0, 0, 135):   18,
    (0, 0, 175):   19,
    (0, 0, 215):   20,
    (0, 0, 255):   12,
    (0, 95, 0):    22,
    (0, 95, 95):   23,
    (0, 95, 135):  24,
    (0, 95, 175):  25,
    (0, 95, 215):  26,
    (0, 95, 255):  27,
    (0, 128, 0):   2,
    (0, 128, 128): 6,
    (0, 135, 0):   28,
    (0, 135, 95):  29,
    (0, 135, 135): 30,
    (0, 135, 175): 31,
    (0, 135, 215): 32,
    (0, 135, 255): 33,
    (0, 175, 0):   34,
    (0, 175, 95):  35,
    (0, 175, 135): 36,
    (0, 175, 175): 37,
    (0, 175, 215): 38,
    (0, 175, 255): 39,
    (0, 215, 0):   40,
    (0, 215, 95):  41,
    (0, 215, 135): 42,
    (0, 215, 175): 43,
    (0, 215, 215): 44,
    (0, 215, 255): 45,
    (0, 255, 0):   46,
    (0, 255, 95):  47,
    (0, 255, 135): 48,
    (0, 255, 175): 49,
    (0, 255, 215): 50,
    (0, 255, 255): 14,
    (8, 8, 8):    232,
    (18, 18, 18): 233,
    (28, 28, 28): 234,
    (38, 38, 38): 235,
    (48, 48, 48): 236,
    (58, 58, 58): 237,
    (68, 68, 68): 238,
    (78, 78, 78): 239,
    (88, 88, 88): 240,
    (95, 0, 0):   52,
    (95, 0, 95):  53,
    (95, 0, 135): 54,
    (95, 0, 175): 55,
    (95, 0, 215): 56,
    (95, 0, 255): 57,
    (95, 95, 0):  58,
    (95, 95, 95):  59,
    (95, 95, 135): 60,
    (95, 95, 175): 61,
    (95, 95, 215): 62,
    (95, 95, 255): 63,
    (95, 135, 0):  64,
    (95, 135, 95): 65,
    (95, 135, 135): 66,
    (95, 135, 175): 67,
    (95, 135, 215): 68,
    (95, 135, 255): 69,
    (95, 175, 0):   70,
    (95, 175, 95) : 71,
    (95, 175, 135): 72,
    (95, 175, 175): 73,
    (95, 175, 215): 74,
    (95, 175, 255): 75,
    (95, 215, 0):   76,
    (95, 215, 95) : 77,
    (95, 215, 135): 78,
    (95, 215, 175): 79,
    (95, 215, 215): 80,
    (95, 215, 255): 81,
    (95, 255, 0):   82,
    (95, 255, 95) : 83,
    (95, 255, 135): 84,
    (95, 255, 175): 85,
    (95, 255, 215): 86,
    (95, 255, 255): 87,
    (98, 98, 98):    241,
    (108, 108, 108): 242,
    (118, 118, 118): 243,
    (128, 0, 0):      1,
    (128, 0, 128):    5,
    (128, 128, 0):    3,
    (128, 128, 128): 244,
    (135, 0, 0):      88,
    (135, 0, 95):     89,
    (135, 0, 135):    90,
    (135, 0, 175):    91,
    (135, 0, 215):    92,
    (135, 0, 255):    93,
    (135, 95, 0):     94,
    (135, 95, 95):    95,
    (135, 95, 135):   96,
    (135, 95, 175):   97,
    (135, 95, 215):   98,
    (135, 95, 255):   99,
    (135, 135, 0):   100,
    (135, 135, 95):  101,
    (135, 135, 135): 102,
    (135, 135, 175): 103,
    (135, 135, 215): 104,
    (135, 135, 255): 105,
    (135, 175, 0):   106,
    (135, 175, 95):  107,
    (135, 175, 135): 108,
    (135, 175, 175): 109,
    (135, 175, 215): 110,
    (135, 175, 255): 111,
    (135, 215, 0):   112,
    (135, 215, 95):  113,
    (135, 215, 135): 114,
    (135, 215, 175): 115,
    (135, 215, 215): 116,
    (135, 215, 255): 117,
    (135, 255, 0):   118,
    (135, 255, 95):  119,
    (135, 255, 135): 120,
    (135, 255, 175): 121,
    (135, 255, 215): 122,
    (135, 255, 255): 123,
    (138, 138, 138): 245,
    (148, 148, 148): 246,
    (158, 158, 158): 247,
    (168, 168, 168): 248,
    (175, 0, 0): 124,
    (175, 0, 95): 125,
    (175, 0, 135): 126,
    (175, 0, 175): 127,
    (175, 0, 215): 128,
    (175, 0, 255): 129,
    (175, 95, 0): 130,
    (175, 95, 95): 131,
    (175, 95, 135): 132,
    (175, 95, 175): 133,
    (175, 95, 215): 134,
    (175, 95, 255): 135,
    (175, 135, 0): 136,
    (175, 135, 95): 137,
    (175, 135, 135): 138,
    (175, 135, 175): 139,
    (175, 135, 215): 140,
    (175, 135, 255): 141,
    (175, 175, 0): 142,
    (175, 175, 95): 143,
    (175, 175, 135): 144,
    (175, 175, 175): 145,
    (175, 175, 215): 146,
    (175, 175, 255): 147,
    (175, 215, 0): 148,
    (175, 215, 95): 149,
    (175, 215, 135): 150,
    (175, 215, 175): 151,
    (175, 215, 215): 152,
    (175, 215, 255): 153,
    (175, 255, 0): 154,
    (175, 255, 95): 155,
    (175, 255, 135): 156,
    (175, 255, 175): 157,
    (175, 255, 215): 158,
    (175, 255, 255): 159,
    (178, 178, 178): 249,
    (188, 188, 188): 250,
    (192, 192, 192): 7,
    (198, 198, 198): 251,
    (208, 208, 208): 252,
    (215, 0, 0): 160,
    (215, 0, 95): 161,
    (215, 0, 135): 162,
    (215, 0, 175): 163,
    (215, 0, 215): 164,
    (215, 0, 255): 165,
    (215, 95, 0): 166,
    (215, 95, 95): 167,
    (215, 95, 135): 168,
    (215, 95, 175): 169,
    (215, 95, 215): 170,
    (215, 95, 255): 171,
    (215, 135, 0): 172,
    (215, 135, 95): 173,
    (215, 135, 135): 174,
    (215, 135, 175): 175,
    (215, 135, 215): 176,
    (215, 135, 255): 177,
    (215, 175, 0): 178,
    (215, 175, 95): 179,
    (215, 175, 135): 180,
    (215, 175, 175): 181,
    (215, 175, 215): 182,
    (215, 175, 255): 183,
    (215, 215, 0): 184,
    (215, 215, 95): 185,
    (215, 215, 135): 186,
    (215, 215, 175): 187,
    (215, 215, 215): 188,
    (215, 215, 255): 189,
    (215, 255, 0): 190,
    (215, 255, 95): 191,
    (215, 255, 135): 192,
    (215, 255, 175): 193,
    (215, 255, 215): 194,
    (215, 255, 255): 195,
    (218, 218, 218): 253,
    (228, 228, 228): 254,
    (238, 238, 238): 255,
    (255, 0, 0): 196,
    (255, 0, 95): 197,
    (255, 0, 135): 198,
    (255, 0, 175): 199,
    (255, 0, 215): 200,
    (255, 0, 255): 13,
    (255, 95, 0): 202,
    (255, 95, 95): 203,
    (255, 95, 135): 204,
    (255, 95, 175): 205,
    (255, 95, 215): 206,
    (255, 95, 255): 207,
    (255, 135, 0): 208,
    (255, 135, 95): 209,
    (255, 135, 135): 210,
    (255, 135, 175): 211,
    (255, 135, 215): 212,
    (255, 135, 255): 213,
    (255, 175, 0): 214,
    (255, 175, 95): 215,
    (255, 175, 135): 216,
    (255, 175, 175): 217,
    (255, 175, 215): 218,
    (255, 175, 255): 219,
    (255, 215, 0): 220,
    (255, 215, 95): 221,
    (255, 215, 135): 222,
    (255, 215, 175): 223,
    (255, 215, 215): 224,
    (255, 215, 255): 225,
    (255, 255, 0): 11,
    (255, 255, 95): 227,
    (255, 255, 135): 228,
    (255, 255, 175): 229,
    (255, 255, 215): 230,
    (255, 255, 255): 231}

def rgb2short(r, g, b):
    """ Find the closest xterm-256 approximation to the given RGB value.
    @param r,g,b: each is a number between 0-255 for the Red, Green, and Blue values
    @returns: integer between 0 and 255, compatible with xterm.
    >>> rgb2short(18, 52, 86)
    23
    >>> rgb2short(255, 255, 255)
    231
    >>> rgb2short(13, 173, 214) # vimeo logo
    38
    :param r:
    :param g:
    :param b:
    """
    incs = (0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff)
    # Break 6-char RGB code into 3 integer vals.
    parts = [ r, g, b] 
    res = []
    for part in parts:
        i = 0
        while i < len(incs)-1:
            s, b = incs[i], incs[i+1]  # smaller, bigger
            if s <= part <= b:
                s1 = abs(s - part)
                b1 = abs(b - part)
                if s1 < b1: closest = s
                else: closest = b
                res.append(closest)
                break
            i += 1
    #print '***', res
    return RGB2SHORT_DICT[tuple(res)]

#---------------------------------------------------------------------

if __name__ == '__main__':
    import doctest
    doctest.testmod()
