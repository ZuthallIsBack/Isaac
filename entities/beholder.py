# entities/beholder.py
import math, pygame
from core.gameobject import MovingObject                     # bez zmian
from utils.anim import SpriteAnim

class Beholder(MovingObject):
    """Boss „Beholder” – identyczna logika jak dotąd,
       ale z animacją śmierci w osobnym sprite-sheecie."""
    SIZE        = (32, 32)
    MAX_HP      = 20
    DEATH_TIME  = 2.5

    # oscylacja salw
    CD_MIN      = 0.1
    CD_MAX      = 0.5
    CD_OSC_SPEED = 0.2
    # wachlarz pocisków
    ROT_SPEED   = 30
    ROT_LIMIT   = 45

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, self.SIZE)

        # --- animacje ---------------------------------------------------
        self.anim      = SpriteAnim("assets/beholder.png",
                                    frames=5, fps=3,  scale=2)
        self.anim_die  = SpriteAnim("assets/beholder_death.png",
                                    frames=5, fps=3,  scale=2)
        # hp / stan
        self.hp         = self.MAX_HP
        self.dying      = False
        self.dead_timer = 0.0

        # oscylacja salw
        self.shoot_period = self.CD_MAX
        self.cd_dir        = -1
        self.shoot_timer   = self.shoot_period
        # oscylacja wachlarza
        self.rot_offset = 0.0
        self.rot_dir    = 1

    # ---------------- obrażenia / śmierć ---------------------------------
    def take_damage(self, dmg=1):
        if self.dying:
            return
        self.hp -= dmg
        if self.hp <= 0:
            self.dying = True

    def is_dead(self) -> bool:
        return self.dying and self.dead_timer >= self.DEATH_TIME

    # ---------------- główna pętla ---------------------------------------
    def update(self, dt: float, player_pos: pygame.Vector2):
        # ─── faza śmierci (identycznie jak Bat, Slime) ───
        if self.dying:
            # odtwarzaj klatki death tylko do ostatniej
            if self.anim_die.index < len(self.anim_die.frames) - 1:
                self.anim_die.update(dt)
            self.dead_timer += dt
            return

        # ─── animacja boss (idle) ───
        self.anim.update(dt)

        # ─── oscylacja kąta wachlarza ───
        self.rot_offset += self.ROT_SPEED * dt * self.rot_dir
        if abs(self.rot_offset) >= self.ROT_LIMIT:
            self.rot_dir *= -1
            self.rot_offset = max(-self.ROT_LIMIT,
                                  min(self.ROT_LIMIT, self.rot_offset))

        # ─── oscylacja firing-rate ───
        self.shoot_period += self.CD_OSC_SPEED * dt * self.cd_dir
        if self.shoot_period <= self.CD_MIN:
            self.shoot_period = self.CD_MIN
            self.cd_dir = 1
        elif self.shoot_period >= self.CD_MAX:
            self.shoot_period = self.CD_MAX
            self.cd_dir = -1

        # ─── strzał, gdy licznik zejdzie do zera ───
        self.shoot_timer -= dt
        if self.shoot_timer <= 0:
            self.shoot_timer += self.shoot_period
            from entities.projectile import Projectile
            from core.game import _current_game

            origin = self.pos + pygame.Vector2(self.SIZE) * 0.5
            for i in range(7):
                base_ang = i * (360 / 7)
                angle    = math.radians(base_ang + self.rot_offset)
                vec      = pygame.Vector2(math.cos(angle), math.sin(angle))
                _current_game.projectiles.append(
                    Projectile(origin, vec, dmg=2, speed=200, owner=self)
                )

    # ---------------- rysowanie ------------------------------------------
    def draw(self, surf: pygame.Surface,
             offset: pygame.Vector2 = pygame.Vector2()):
        img = self.anim_die.image if self.dying else self.anim.image
        surf.blit(img, self.rect.move(offset))
