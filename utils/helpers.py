import math
from bisect import bisect_right
from core.settings import COMBO_MAP

def clamp(v, lo, hi):
    return lo if v < lo else (hi if v > hi else v)

def clamp_color(r, g, b):
    return (clamp(r, 0, 255), clamp(g, 0, 255), clamp(b, 0, 255))

def lerp_color(c0, c1, t):
    return (
        int(c0[0] + (c1[0] - c0[0]) * t),
        int(c0[1] + (c1[1] - c0[1]) * t),
        int(c0[2] + (c1[2] - c0[2]) * t),
    )

def level_threshold(level):
    return (20 + level * 6) * level

def get_combo_multiplier(combo):
    # 0-2: 1x, 3-6: 1.5x, 7-11: 2x, 12-17: 2.5x, 18-24: 3x, 25+: 4x
    if combo < 3:
        return 1.0
    elif combo < 7:
        return 1.5
    elif combo < 12:
        return 2.0
    elif combo < 18:
        return 2.5
    elif combo < 25:
        return 3.0
    else:
        return 4.0

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
