<p align="center">
  <img src="https://img.shields.io/github/stars/VIDAKHOSHPEY22/Atari-Racer?style=for-the-badge&logo=github&color=ff6b6b" alt="Stars" />
  <img src="https://img.shields.io/github/license/VIDAKHOSHPEY22/Atari-Racer?style=for-the-badge&color=95e1d3" alt="Licence" />
  <img src="https://img.shields.io/github/last-commit/VIDAKHOSHPEY22/Atari-Racer?style=for-the-badge&color=a8e6cf" alt="Last Commit" />
  <img src="https://img.shields.io/github/v/release/VIDAKHOSHPEY22/Atari-Racer?style=for-the-badge&color=ffd93d" alt="Latest Release" />
</p>

<h1 align="center">ATARI RACER</h1>

<h3 align="center">A 2D endless racing game built with Python</h3>

---

## About the Project

ATARI RACER is an exciting arcade-style racing game where you dodge traffic, collect coins, and set high scores. The game features 3 difficulty levels, 10 car skins with unique speed bonuses, boost mechanics and a combo multiplier system.

---

## Quick Start

```bash
git clone https://github.com/VIDAKHOSHPEY22/Atari-Racer.git
cd Atari-Racer
pip install -r requirements.txt
python atari.py
```

---

## Features

| Feature | Description |
|---------|-------------|
| Car Skins | 10 different skins with unique speed bonuses |
| Boost System | Press SPACE to activate speed boost (costs 50 points) |
| Combo Multiplier | Chain obstacles and coins for multipliers up to x4 |
| Sound Effects | Procedurally generated audio for coins, boost, hits, and more |
| Particle Effects | Explosions, sparks, and boost trail effects |
| Power-Up | Shield pickups |
| Difficulty Levels | Easy, Medium, and Hard |
| High Score | Automatically saves your best score |
| Garage Upgrades | Spend coins on permanent speed and life upgrades |

---

## Controls

| Key | Action |
|-----|--------|
| ← → | Steer left / right |
| SPACE | Boost |
| P | Pause / Resume |
| R | Restart |

---

## Latest Version - V5.6

- Removed the police chase mechanic to keep the core dodge-and-collect loop tighter
- Removed the Magnet power-up; Shield and Time Freeze remain
- Removed screen shake on collisions for a calmer, steadier camera
- Removed fog weather, Cone and the Speed Bump hazard to simplify the hazard set down to Barrier and Oil Slick
- Reduced the particle pool size to match the trimmed effect set
- Corrected the README to no longer claim dynamic responsive resizing, since the window size is currently fixed
- Updated `Checklist.md` to track these changes
- Renamed from racing-car-game to Atari-Racer for clarity
- Bump pip/github actions stuff
- Removed the rain weather effect and RainPool system to simplify the gameplay loop
- Reduced the car skin roster from 15 to 10 and renamed all skins for a more professional tone
- Updated to Python 3.14 support and fixed sound bug

---

## Gameplay Preview

<p align="center">
  <img src="screenshots/new-preview.gif" width="90%" alt="Gameplay Preview">
</p>

---

## Screenshots

### Menu

<p align="center">
  <img src="screenshots/new-menu.png" width="90%" alt="Menu">
</p>

### Gameplay

<p align="center">
  <img src="screenshots/new-game.png" width="90%" alt="Gameplay">
</p>

### Game Over

<p align="center">
  <img src="screenshots/new-end.png" width="90%" alt="Game Over">
</p>

---

## Installation

### Dependencies
- Python 3.13
- pygame-ce
- numpy (optional, used for sound effects)

### pip installation

```bash
pip install pygame-ce
```

For sound effects:
```bash
pip install pygame-ce numpy
```

---

## Building Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed atari.py
```

---

## Contributors
<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/TheM1ddleM1n">
        <img src="https://github.com/TheM1ddleM1n.png?size=80" width="70" height="70" style="border-radius:50%;" />
        <br />
        <b>👑 TheM1ddleM1n</b>
      </a>
      <br />
      <img src="https://img.shields.io/badge/-Co--Owner-blue?style=flat-square" />
    </td>
  </tr>
</table>
<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com">
        <img src="https://github.com/procopioos.png?size=80" width="70" height="70" style="border-radius:50%;" />
        <br />
        <b>👑 procopioos</b>
      </a>
      <br />
      <img src="https://img.shields.io/badge/-Core%20Contributor-d4af37?style=flat-square" /><br />
    </td>
    <td align="center">
      <a href="https://github.com/Esmaili963">
        <img src="https://github.com/Esmaili963.png?size=80" width="70" height="70" style="border-radius:50%;" />
        <br />
        <b>👑 Esmaili963</b>
      </a>
      <br />
      <img src="https://img.shields.io/badge/-Core%20Contributor-d4af37?style=flat-square" /><br />
    </td>
    <td align="center">
      <a href="https://github.com/YALDAKHOSHPEY">
        <img src="https://github.com/YALDAKHOSHPEY.png?size=80" width="70" height="70" style="border-radius:50%;" />
        <br />
        <b>Yalda</b>
      </a>
      <br />
      <small>Contributor</small>
    </td>
    <td align="center">
      <a href="https://github.com/anannyami">
        <img src="https://github.com/anannyami.png?size=80" width="70" height="70" style="border-radius:50%;" />
        <br />
        <b>Ananya</b>
      </a>
      <br />
      <small>Contributor</small>
    </td>
    <td align="center">
      <a href="https://github.com/saurav714">
        <img src="https://github.com/saurav714.png?size=80" width="70" height="70" style="border-radius:50%;" />
        <br />
        <b>Saurav</b>
      </a>
      <br />
      <small>Contributor</small>
    </td>
    <td align="center">
      <a href="https://github.com/mukeshlilawat1">
        <img src="https://github.com/mukeshlilawat1.png?size=80" width="70" height="70" style="border-radius:50%;" />
        <br />
        <b>Mukesh</b>
      </a>
      <br />
      <small>Contributor</small>
    </td>
  </tr>
</table>


---

## Contact Me

Email: vidatwin18@gmail.com

---

## License

This project is licensed under MIT.

---

<div align="center">

**Ready, Set, GO!**

</div>
