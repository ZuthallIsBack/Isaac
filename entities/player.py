"""Implementacja sterowanej przez użytkownika postaci."""
import pygame
from core.gameobject import MovingObject

class Player(MovingObject):
    SPEED = 200  # piksele na sekundę
    COLOR = (180, 180, 255)
    SIZE = (32, 32)
    MAX_HP = 3
    COOLDOWN = 0.25  # s
    HIT_COOLDOWN = 1.0

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, self.SIZE)
        self.cooldown = 0.0
        self.hp = self.MAX_HP
        self.hit_cd = 0.0  # timer invincibility

    # ───────── shooting helpers ──────────────────────────
    def can_shoot(self) -> bool:
        return self.cooldown <= 0.0

    def reset_cooldown(self) -> None:
        self.cooldown = self.COOLDOWN

    # ───────── damage helper ─────────────────────────
    def hurt(self, dmg: int = 1) -> bool:
        """Zwraca True, jeśli faktycznie odebrano życie."""
        if self.hit_cd <= 0.0 and self.hp > 0:
            self.hp = max(0, self.hp - dmg)
            self.hit_cd = self.HIT_COOLDOWN
            return True
        return False

    # ──────────────────────────────────────────────────────────── API ────────
    def handle_event(self, event: pygame.event.Event) -> None:
        """Na razie nic nie robi – sterowanie zbieramy w update()."""
        pass

    def update(self, dt: float) -> None:
        self.cooldown = max(0.0, self.cooldown - dt)
        self.hit_cd = max(0.0, self.hit_cd - dt)
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        # góra / dół
        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1

        # lewo / prawo
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_d]:
            direction.x += 1

        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.pos += direction * self.SPEED * dt
            self.rect.topleft = self.pos

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2()):
        pygame.draw.rect(surface, self.COLOR, self.rect.move(offset))