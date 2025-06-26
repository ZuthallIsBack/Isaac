import pygame
from core.gameobject import GameObject


import pygame
from utils.anim import SpriteAnim
from core.gameobject import GameObject

class Heart(GameObject):
    def __init__(self, pos: tuple[int, int]):
        if not hasattr(Heart, "_ANIM"):
            Heart._ANIM = SpriteAnim("assets/heart_pickup.png",
                                         frames=2, fps=6, scale=2)
        w, h = Heart._ANIM.image.get_size()
        super().__init__(pos, (w, h))

    def update(self, dt: float) -> None:
        Heart._ANIM.update(dt)

    def draw(self, surf: pygame.Surface, offset=pygame.Vector2()) -> None:
        surf.blit(Heart._ANIM.image, self.rect.move(offset))

