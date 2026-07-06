import pygame as pg
import numpy as np
from core.settings import HAS_NUMPY

class SoundManager:
    def __init__(self):
        pg.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = self._build_sounds()
    
    def _make_sound(self, wave):
        if not HAS_NUMPY:
            return self._dummy_sound()
        n = len(wave)
        arr = np.array(wave * 32767, dtype=np.int16)
        return pg.sndarray.make_sound(np.repeat(arr.reshape(n, 1), 2, axis=1))
    
    def _dummy_sound(self):
        class Dummy:
            def play(self): pass
        return Dummy()
    
    def _build_sounds(self):
        if not HAS_NUMPY:
            dummy = self._dummy_sound()
            return {k: dummy for k in ("coin", "boost", "levelup", "hit", "explosion", "powerup")}
        
        sr = 22050
        
        def _buf(duration):
            n = int(sr * duration)
            return n, np.arange(n) / sr
        
        n, t = _buf(0.15)
        freq = 800 * np.exp(-t * 8)
        coin = self._make_sound(np.sin(2 * np.pi * freq * t) * np.exp(-t * 15) * 0.6)
        
        n, t = _buf(0.8)
        freq = 300 + 400 * t / 0.8
        boost = self._make_sound(np.sin(2 * np.pi * freq * t) * np.exp(-t * 3) * 0.76)
        
        n, t = _buf(0.6)
        levelup = self._make_sound(
            (np.sin(2 * np.pi * 440 * t) * np.exp(-t * 2) +
             np.sin(2 * np.pi * 880 * t) * np.exp(-t * 3)) * 0.61
        )
        
        n, t = _buf(0.2)
        noise = np.random.normal(0, 1, n) * np.exp(-t * 20)
        tone = np.sin(2 * np.pi * 200 * t) * np.exp(-t * 15)
        hit = self._make_sound((noise * 0.6 + tone * 0.4) * np.exp(-t * 10) * 0.46)
        
        n, t = _buf(0.5)
        noise = np.random.normal(0, 1, n) * np.exp(-t * 15)
        explosion = self._make_sound(noise * 0.24)
        
        n, t = _buf(0.5)
        freq = 500 + 700 * t / 0.5
        powerup = self._make_sound(
            (np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2 * t)) * np.exp(-t * 4) * 0.67
        )
        
        return dict(coin=coin, boost=boost, levelup=levelup, 
                   hit=hit, explosion=explosion, powerup=powerup)
    
    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
