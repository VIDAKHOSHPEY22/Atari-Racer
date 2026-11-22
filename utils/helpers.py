import math

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
    return level * 750

def get_time_multiplier(time_survived):
    if time_survived < 30:
        return 1.0
    elif time_survived < 60:
        return 1.5
    elif time_survived < 90:
        return 2.0
    elif time_survived < 120:
        return 2.5
    elif time_survived < 150:
        return 3.0
    else:
        return 4.0

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
