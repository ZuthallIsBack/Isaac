import pygame


class HUD:
    HEART_W = 20
    HEART_H = 20
    GAP = 4

    def __init__(self, max_hp: int):
        self.max_hp = max_hp

    def draw(self, surface: pygame.Surface, hp: int) -> None:
        for i in range(self.max_hp):
            color = (220, 70, 70) if i < hp else (60, 60, 60)
            x = 16 + i * (self.HEART_W + self.GAP)
            pygame.draw.rect(surface, color, (x, 10, self.HEART_W, self.HEART_H))
