# audio.py
import pygame
from pathlib import Path

_ASSET_DIR = Path(__file__).with_suffix('').parent / "assets" / "audio"
_BG_MUSIC = _ASSET_DIR / "background.mp3" # It's "background.mp3" dowloaded from: https://freemusicarchive.org/music/lenny-pixels/digital-groove-system-vol2/motherboard-encore-8bit/


pygame.mixer.init()

def play_music(loop: bool = True, volume: float = 0.2):
    """Uruchamia lub wznawia muzykę w tle."""
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(_BG_MUSIC)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1 if loop else 0)

def toggle_music():
    if pygame.mixer.music.get_pos() == -1:
        play_music()            # nic nie gra → start
    elif pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()   # gra → pauza
    else:
        pygame.mixer.music.unpause() # pauza → gra

