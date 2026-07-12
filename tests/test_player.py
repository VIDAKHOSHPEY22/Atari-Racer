import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pygame
from entities.player import Player
from data.skins import Skin
from core.settings import ROAD_LEFT, ROAD_RIGHT

class MockKeys:
    """Minimal stand-in for pygame.key.get_pressed()."""
    def __init__(self, left=False, right=False):
        self._data = {
            pygame.K_LEFT: 1 if left else 0,
            pygame.K_RIGHT: 1 if right else 0,
        }

    def __getitem__(self, key):
        return self._data.get(key, 0)

@pytest.fixture
def player():
    skin = Skin("Test", (255, 0, 0), "sedan", 1.0)
    return Player(skin, speed_level=0)

def test_player_initial_position(player):
    expected_x = (800 // 2 - player.WIDTH // 2)
    assert player.x == expected_x
    assert player.y == (600 - player.HEIGHT - 30)

def test_player_movement_left(player):
    keys = MockKeys(left=True)
    player.update(0.1, keys)
    assert player.vel_x < 0
    assert player.x > ROAD_LEFT

def test_player_movement_right(player):
    keys = MockKeys(right=True)
    player.update(0.1, keys)
    assert player.vel_x > 0

def test_player_boost_application(player):
    player.apply_boost()
    assert player.boost_timer == 1.5
    assert player.boost_multiplier == 1.8

def test_player_speed_factor(player):
    assert player.get_speed_factor() == 1.0
    player.apply_boost()
    assert player.get_speed_factor() == 1.8
    player2 = Player(Skin("Test2", (0,255,0), "sedan", 1.0), speed_level=1)
    assert player2.get_speed_factor() == 1.0 + 0.04

def test_player_clamp_within_road(player):
    player.x = ROAD_LEFT - 10
    keys = MockKeys()
    player.update(0.1, keys)
    assert player.x >= ROAD_LEFT

    player.x = ROAD_RIGHT + 10
    player.update(0.1, keys)
    assert player.x <= ROAD_RIGHT - player.WIDTH
