"""Implementacja sterowanej przez użytkownika postaci."""
import pygame
from core.gameobject import MovingObject

class Player(MovingObject):
    SPEED = 200  # piksele na sekundę
    COLOR = (180, 180, 255)
    SIZE = (32, 32)
    MAX_HP = 3
    COOLDOWN = 0.25  # s

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, self.SIZE)
        self.cooldown = 0.0
        self.hp = self.MAX_HP

    # ───────── shooting helpers ──────────────────────────
    def can_shoot(self) -> bool:
        return self.cooldown <= 0.0

    def reset_cooldown(self) -> None:
        self.cooldown = self.COOLDOWN

    # ──────────────────────────────────────────────────────────── API ────────
    def handle_event(self, event: pygame.event.Event) -> None:
        """Na razie nic nie robi – sterowanie zbieramy w update()."""
        pass

    def update(self, dt: float) -> None:
        self.cooldown = max(0.0, self.cooldown - dt)
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        # góra / dół
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y += 1

        # lewo / prawo
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x += 1

        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.pos += direction * self.SPEED * dt
            self.rect.topleft = self.pos

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2()):
        pygame.draw.rect(surface, self.COLOR, self.rect.move(offset))