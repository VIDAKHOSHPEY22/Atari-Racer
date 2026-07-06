import os
from utils.helpers import clamp

def load_high_score():
    try:
        with open("highscore.txt") as f:
            value = f.read().strip()
        score = int(value)
        return score if score > 0 else 0
    except (FileNotFoundError, ValueError, OSError):
        return 0

def save_high_score(score):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
    except OSError:
        pass

def load_progress():
    wallet, speed_level, life_level = 0, 0, 0
    try:
        with open("progress.txt") as f:
            parts = f.read().strip().split(",")
        if len(parts) >= 3:
            wallet = max(0, int(parts[0]))
            speed_level = clamp(int(parts[1]), 0, 5)
            life_level = clamp(int(parts[2]), 0, 2)
    except (FileNotFoundError, ValueError, OSError):
        pass
    return wallet, {"speed": speed_level, "life": life_level}

def save_progress(wallet, upgrades):
    try:
        with open("progress.txt", "w") as f:
            f.write(f"{wallet},{upgrades['speed']},{upgrades['life']}")
    except OSError:
        pass
