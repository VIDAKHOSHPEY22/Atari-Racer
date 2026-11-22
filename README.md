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

ATARI RACER is an arcade-style endless racer where you dodge traffic, collect coins, and chase high scores. Survive as long as possible, as the longer you last, the faster it gets and the more your coins are worth.

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
| Car Skins | 6 distinct skins with unique color schemes |
| Boost System | Press SPACE to activate speed boost (costs 100 points) |
| Time Multiplier | Score multiplier increases every 30 seconds survived |
| Progressive Difficulty | Speed and obstacle frequency ramp up over time |
| Sound Effects | Procedurally generated audio for coins, boost, hits, and more |
| Particle Effects | Coin and hit burst effects |
| Achievements | 16 achievements to unlock |
| High Score | Automatically saves your best score |
| Garage Upgrades | Spend coins on permanent speed and life upgrades |

---

## Controls

| Key | Action |
|-----|--------|
| ← → | Steer left / right |
| SPACE | Boost (costs 100 pts) |
| P | Pause / Resume |
| R | Restart |

---

## Scoring

Coins are your primary score source. The longer you survive, the higher your multiplier:

| Time Survived | Multiplier |
|---------------|------------|
| 0 – 29s | x1.0 |
| 30 – 59s | x1.5 |
| 60 – 89s | x2.0 |
| 90 – 119s | x2.5 |
| 120 – 149s | x3.0 |
| 150s+ | x4.0 |

---

## Achievements

| Achievement | Condition |
|-------------|-----------|
| Pocket Change | Collect your first coin |
| Coin Collector | Collect 100 coins lifetime |
| Coin Hoarder | Collect 1000 coins lifetime |
| Rookie Racer | Score 500 in one run |
| Road Legend | Score 2000 in one run |
| Apex Racer | Score 5000 in one run |
| Dedicated Driver | Play 25 runs |
| Minute Man | Survive 60 seconds in one run |
| Endurance | Survive 180 seconds in one run |
| Immortal | Survive 300 seconds in one run |
| Nitro Junkie | Use boost 10 times |
| Getting Serious | Reach level 5 |
| Elite | Reach level 10 |
| Unlucky | Die at level 1 |
| Untouchable | Complete a run without getting hit |
| Big Spender | Spend 500 coins in the garage |

---

## Car Skins

| Skin | Vibe |
|------|------|
| Stealth | Matte black with red accents |
| Rally | White with yellow roof and blue accents |
| Retro | Cream body with brown roof |
| Viper | Deep red with orange accents |
| Arctic | Ice blue with cyan accents |
| Phantom | Dark purple with pink accents |

---

## Installation

### Dependencies
- Python 3.13+
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
  </tr>
</table>

---

## Contact

Email: vidatwin18@gmail.com

---

## License

This project is licensed under MIT.
