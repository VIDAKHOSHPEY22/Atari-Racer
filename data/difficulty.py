from collections import namedtuple

DiffSettings = namedtuple("DiffSettings", "base_speed obs_interval speed_inc obs_speed")

DIFFICULTY = {
    "Easy": DiffSettings(280, 1.8, 6, (220, 320)),
    "Medium": DiffSettings(380, 1.3, 9, (280, 400)),
    "Hard": DiffSettings(500, 0.9, 12, (350, 500)),
}