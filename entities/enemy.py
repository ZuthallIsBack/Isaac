import pygame
from core.gameobject import MovingObject


class Charger(MovingObject):
    SIZE = (28, 28)
    COLOR = (200, 60, 60)
    SPEED = 120
    MAX_HP = 3

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, self.SIZE)
        self.hp = self.MAX_HP

    def update(self, dt: float, target_pos: pygame.Vector2) -> None:
        direction = target_pos - self.pos
        if direction.length_squared() > 0:
            self.pos += direction.normalize() * self.SPEED * dt
            self.rect.topleft = self.pos

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2()) -> None:
        pygame.draw.rect(surface, self.COLOR, self.rect.move(offset))

    # zwraca True, jeśli zginął
    def take_damage(self, dmg: int = 1) -> bool:
        self.hp -= dmg
        return self.hp <= 0
