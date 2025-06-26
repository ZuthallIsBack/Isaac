"""Pociski wystrzeliwane przez różne bronie (łza, strzała itd.)."""

from __future__ import annotations
import math, pygame
from core.gameobject import MovingObject
from entities.weapon import Weapon

class Projectile(MovingObject):
    SIZE = (8, 8)                # kolider – nie skalujemy

    # ───────────────────────── INIT ──────────────────────────
    def __init__(
        self,
        pos: tuple[int, int],
        direction: pygame.Vector2,
        weapon: Weapon = Weapon.TEARS,
        dmg: int = 1,
        speed: int = 450
    ):
        # lazy-load sprite’ów
        if not hasattr(Projectile, "_SPRITES"):
            Projectile._SPRITES = {
                Weapon.TEARS: pygame.image.load("assets/tear.png").convert_alpha(),
                Weapon.BOW:   pygame.image.load("assets/arrow.png").convert_alpha(),
            }

        super().__init__(pos, self.SIZE)

        # parametry pocisku
        self.weapon = weapon
        self.dmg    = dmg
        self.speed  = speed
        self.direction = pygame.Vector2(direction).normalize()

        # wybór sprite’a + obrót w stronę lotu
        base_img   = Projectile._SPRITES.get(weapon, Projectile._SPRITES[Weapon.TEARS])
        angle_deg  = -math.degrees(math.atan2(self.direction.y, self.direction.x))
        self.image = pygame.transform.rotate(base_img, angle_deg)
        self.rect  = self.image.get_rect(center=self.pos)

    # ─────────────────────── update / draw ─────────────────────
    def update(self, dt: float) -> None:
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = self.pos

    def draw(self, surf: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2()) -> None:
        surf.blit(self.image, self.rect.move(offset))
