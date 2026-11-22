import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.helpers import clamp, clamp_color, level_threshold, get_time_multiplier

def test_clamp():
    assert clamp(5, 0, 10) == 5
    assert clamp(-1, 0, 10) == 0
    assert clamp(11, 0, 10) == 10
    assert clamp(0, 0, 10) == 0
    assert clamp(10, 0, 10) == 10

def test_clamp_color():
    assert clamp_color(300, -10, 150) == (255, 0, 150)
    assert clamp_color(100, 200, 50) == (100, 200, 50)
    assert clamp_color(-5, 256, 0) == (0, 255, 0)

def test_level_threshold():
    assert level_threshold(1) == 750
    assert level_threshold(2) == 1500
    assert level_threshold(3) == 2250
    assert level_threshold(4) == 3000
    assert level_threshold(5) == 3750

def test_get_time_multiplier():
    assert get_time_multiplier(0) == 1.0
    assert get_time_multiplier(29) == 1.0
    assert get_time_multiplier(30) == 1.5
    assert get_time_multiplier(59) == 1.5
    assert get_time_multiplier(60) == 2.0
    assert get_time_multiplier(89) == 2.0
    assert get_time_multiplier(90) == 2.5
    assert get_time_multiplier(119) == 2.5
    assert get_time_multiplier(120) == 3.0
    assert get_time_multiplier(149) == 3.0
    assert get_time_multiplier(150) == 4.0
    assert get_time_multiplier(999) == 4.0
