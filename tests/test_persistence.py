import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tempfile
import shutil
from utils import persistence

def _isolated_cwd():
    tmp_dir = tempfile.mkdtemp()
    old_cwd = os.getcwd()
    os.chdir(tmp_dir)
    return old_cwd, tmp_dir

def test_high_score_save_load():
    old_cwd, tmp_dir = _isolated_cwd()
    try:
        persistence.save_high_score(150)
        assert persistence.load_high_score() == 150
    finally:
        os.chdir(old_cwd)
        shutil.rmtree(tmp_dir)

def test_high_score_load_missing_file():
    old_cwd, tmp_dir = _isolated_cwd()
    try:
        assert persistence.load_high_score() == 0
    finally:
        os.chdir(old_cwd)
        shutil.rmtree(tmp_dir)

def test_high_score_load_negative_value():
    old_cwd, tmp_dir = _isolated_cwd()
    try:
        with open("highscore.txt", "w") as f:
            f.write("-40")
        assert persistence.load_high_score() == 0
    finally:
        os.chdir(old_cwd)
        shutil.rmtree(tmp_dir)

def test_progress_save_load():
    old_cwd, tmp_dir = _isolated_cwd()
    try:
        upgrades = {"speed": 3, "life": 1}
        persistence.save_progress(220, upgrades)
        wallet, loaded = persistence.load_progress()
        assert wallet == 220
        assert loaded == upgrades
    finally:
        os.chdir(old_cwd)
        shutil.rmtree(tmp_dir)

def test_progress_load_missing_file():
    old_cwd, tmp_dir = _isolated_cwd()
    try:
        wallet, upgrades = persistence.load_progress()
        assert wallet == 0
        assert upgrades == {"speed": 0, "life": 0}
    finally:
        os.chdir(old_cwd)
        shutil.rmtree(tmp_dir)

def test_progress_load_clamps_out_of_range_levels():
    old_cwd, tmp_dir = _isolated_cwd()
    try:
        with open("progress.txt", "w") as f:
            f.write("50,99,-5")
        wallet, upgrades = persistence.load_progress()
        assert wallet == 50
        assert upgrades == {"speed": 5, "life": 0}
    finally:
        os.chdir(old_cwd)
        shutil.rmtree(tmp_dir)
