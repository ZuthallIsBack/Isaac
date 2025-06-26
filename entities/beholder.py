# entities/beholder.py
import math, pygame
from core.gameobject import MovingObject
from utils.anim       import SpriteAnim

class Beholder(MovingObject):
    """
    Boss „Beholder” – animowany ze 5 klatek (32×32), stoi w miejscu,
    co określony czas wypluwa 7 pocisków wachlarzem, który oscyluje
    w prawo/lewo, a sam czas pomiędzy strzałami zmienia się
    płynnie między 0.1 a 0.5 sekundy.
    """
    SIZE        = (32, 32)
    MAX_HP      = 20
    DEATH_TIME  = 1.0

    # zakres okresu między salwami
    CD_MIN      = 0.1    # najszybszy firing rate (co 0.1s)
    CD_MAX      = 0.5    # najwolniejszy firing rate (co 0.5s)
    CD_OSC_SPEED= 0.2    # zmiana okresu o 0.2s na sekundę

    ROT_SPEED   = 30     #°/s prędkość obrotu wachlarza
    ROT_LIMIT   = 45     #° maksymalne odchylenie wachlarza

    def __init__(self, pos: tuple[int,int]):
        super().__init__(pos, self.SIZE)
        self.anim = SpriteAnim("assets/beholder.png", frames=5, fps=5, scale=2)

        self.hp           = self.MAX_HP
        self.dying        = False
        self.dead_timer   = 0.0

        # ─── oscylacja firing rate ───
        self.shoot_period = self.CD_MAX   # startujemy od najwolniejszego
        self.cd_dir       = -1            # -1 = zwalniamy w kierunku CD_MIN
        self.shoot_timer  = self.shoot_period

        # ─── oscylacja wachlarza ───
        self.rot_offset = 0.0
        self.rot_dir    = 1

    def take_damage(self, dmg=1):
        if self.dying:
            return
        self.hp -= dmg
        if self.hp <= 0:
            self.dying = True

    def is_dead(self) -> bool:
        return self.dying and self.dead_timer >= self.DEATH_TIME

    def update(self, dt: float, player_pos: pygame.Vector2):
        # ─── śmierć ───
        if self.dying:
            if self.anim.index < len(self.anim.frames) - 1:
                self.anim.update(dt)
            self.dead_timer += dt
            return

        # ─── animacja boss ───
        self.anim.update(dt)

        # ─── oscylacja kąta wachlarza ───
        self.rot_offset += self.ROT_SPEED * dt * self.rot_dir
        if abs(self.rot_offset) >= self.ROT_LIMIT:
            self.rot_dir   *= -1
            self.rot_offset = max(-self.ROT_LIMIT,
                                  min(self.ROT_LIMIT, self.rot_offset))

        # ─── oscylacja firing rate ───
        self.shoot_period += self.CD_OSC_SPEED * dt * self.cd_dir
        if self.shoot_period <= self.CD_MIN:
            self.shoot_period = self.CD_MIN
            self.cd_dir       = 1
        elif self.shoot_period >= self.CD_MAX:
            self.shoot_period = self.CD_MAX
            self.cd_dir       = -1

        # ─── odliczanie do salwy ───
        self.shoot_timer -= dt
        if self.shoot_timer <= 0:
            # ustaw następne odliczanie na bieżący okres
            self.shoot_timer += self.shoot_period

            from entities.projectile import Projectile
            from core.game import _current_game

            origin = self.pos + pygame.Vector2(self.SIZE) * 0.5

            # wystrzel 7 pocisków wachlarzem + rot_offset
            for i in range(7):
                base_ang = i * (360 / 7)
                angle    = math.radians(base_ang + self.rot_offset)
                dir_vec  = pygame.Vector2(math.cos(angle), math.sin(angle))
                proj = Projectile(
                    origin,
                    dir_vec,
                    dmg=2,
                    speed=200,
                    owner=self
                )
                _current_game.projectiles.append(proj)

    def draw(self, surf: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2()):
        img = self.anim.image
        pos = self.rect.move(offset).topleft
        surf.blit(img, pos)
