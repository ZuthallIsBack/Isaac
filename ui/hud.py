import pygame
from utils.anim import SpriteAnim   # już istnieje? jeśli nie – dodaj import

class HUD:
    def __init__(self, max_hp: int):
        self.max_hp = max_hp
        self.ICON   = pygame.transform.scale(
            pygame.image.load("assets/heart_hud.png").convert_alpha(), (24, 24))

    def draw(self, surf: pygame.Surface, hp: int) -> None:
        for i in range(self.max_hp):
            x = 16 + i*28
            y = 16
            img = self.ICON.copy()
            if i >= hp:                       # puste serce ⇒ wyszarz
                img.set_alpha(60)
            surf.blit(img, (x, y))
