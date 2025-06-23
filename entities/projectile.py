import pygame
from core.gameobject import MovingObject


class Projectile(MovingObject):
    SIZE = (8, 8)
    COLOR = (170, 200, 255)
    SPEED = 450

    def __init__(self, pos: tuple[int, int], direction: pygame.Vector2):
        super().__init__(pos, self.SIZE)
        self.direction = direction.normalize()

    def update(self, dt: float) -> None:
        self.pos += self.direction * self.SPEED * dt
        self.rect.topleft = self.pos

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2()) -> None:
        pygame.draw.rect(surface, self.COLOR, self.rect.move(offset))
