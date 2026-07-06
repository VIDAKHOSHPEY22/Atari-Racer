import pygame as pg

WIDTH, HEIGHT = 800, 600
FPS = 60

BLACK = (10, 10, 10)
WHITE = (240, 240, 240)
GRAY = (100, 100, 100)
RED = (220, 50, 50)
GREEN = (50, 200, 80)
BLUE = (50, 120, 220)
YELLOW = (240, 210, 40)
CYAN = (50, 210, 210)
ORANGE = (255, 140, 0)
PURPLE = (170, 60, 180)
PINK = (255, 100, 170)
ROAD_COLOR = (35, 35, 40)
SHOULDER_COLOR = (60, 62, 58)
GRASS_COLOR = (45, 75, 40)

ROAD_LEFT, ROAD_RIGHT = 150, 650
LANE_CENTERS = [212, 325, 437, 550]

COIN_BASE_VALUE = 5
POWERUP_SHIELD = "shield"
POWERUP_TIMEFREEZE = "timefreeze"

POWERUP_META = {
    POWERUP_SHIELD: ((80, 180, 255), "SHIELD", 6.0),
    POWERUP_TIMEFREEZE: ((80, 230, 200), "FREEZE", 5.0),
}

_COMBO_THRESHOLDS = (3, 7, 12, 18, 25)
_COMBO_MULTIPLIERS = (1.5, 2.0, 2.5, 3.0, 4.0)
COMBO_MAP = {t: m for t, m in zip(_COMBO_THRESHOLDS, _COMBO_MULTIPLIERS)}

WEATHER_CLEAR = "clear"
WEATHER_RAIN = "rain"

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
