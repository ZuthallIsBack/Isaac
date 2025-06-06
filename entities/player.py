"""Implementacja sterowanej przez użytkownika postaci."""
import pygame
from core.gameobject import MovingObject


class Player(MovingObject):
    SPEED = 200  # piksele na sekundę
    COLOR = (180, 180, 255)
    SIZE = (32, 32)

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, self.SIZE)

    # ──────────────────────────────────────────────────────────── API ────────
    def handle_event(self, event: pygame.event.Event) -> None:
        """Na razie nic nie robi – sterowanie zbieramy w update()."""
        pass

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_d]:
            direction.x += 1

        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.pos += direction * self.SPEED * dt
            self.rect.topleft = self.pos

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.COLOR, self.rect)