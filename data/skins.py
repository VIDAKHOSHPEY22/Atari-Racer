from collections import namedtuple
from core.settings import BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE, CYAN, PINK

Skin = namedtuple("Skin", "name color type speed_bonus")

CAR_SKINS = [
    Skin("Blue Racer", BLUE, "sedan", 1.0),
    Skin("Red Speedster", RED, "sedan", 1.1),
    Skin("Green Machine", GREEN, "suv", 0.95),
    Skin("Yellow Lightning", YELLOW, "sedan", 1.15),
    Skin("Purple Power", PURPLE, "suv", 1.0),
    Skin("Orange Blaze", ORANGE, "truck", 0.9),
    Skin("Cyan Cruiser", CYAN, "sedan", 1.05),
    Skin("Pink Dream", PINK, "suv", 1.0),
    Skin("Ghost White", (230, 230, 235), "sedan", 1.08),
    Skin("Midnight Black", (25, 25, 30), "sedan", 1.12),
    Skin("Lime Rocket", (160, 230, 30), "sedan", 1.18),
    Skin("Crimson Truck", (180, 20, 40), "truck", 0.88),
    Skin("Steel SUV", (140, 160, 175), "suv", 0.97),
    Skin("Gold Rush", (212, 175, 55), "sedan", 1.13),
    Skin("Neon Violet", (138, 43, 226), "suv", 1.02),
]