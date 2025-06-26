"""Gracz sterowany klawiaturą: ruch, strzał, obrażenia, animacje."""
from __future__ import annotations
import pygame
from pygame import Vector2
from core.gameobject     import MovingObject
from utils.anim          import SpriteAnim
from entities.weapon     import Weapon, WEAPON_CFG
from entities.projectile import Projectile
from entities.sword_sweep import SwordSweep


class Player(MovingObject):
    # ────────── STAŁE ──────────
    SIZE          = (32, 32)
    SPEED         = 200
    MAX_HP        = 3
    COOLDOWN_HIT  = 1.0
    SLOW_FACTOR   = 0.5
    SLOW_DURATION = 1.0
    DEATH_TIME    = 1.5

    # ────────── INIT ──────────
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, self.SIZE)

        # Timery
        self.cool_shot = 0.0
        self.cool_hit  = 0.0
        self.slow_t    = 0.0
        self.dead_t    = 0.0

        self.hp   = self.MAX_HP
        self.dead = False

        # Animacje
        self.anim_idle = SpriteAnim("assets/player_idle.png",       frames=1, fps=6, scale=2)
        self.anim_side = SpriteAnim("assets/player_walk.png",       frames=3, fps=8, scale=2)
        self.anim_up   = SpriteAnim("assets/player_walk_up.png",    frames=3, fps=8, scale=2)
        self.anim_down = SpriteAnim("assets/player_walk_down.png",  frames=3, fps=8, scale=2)
        self.anim_die  = SpriteAnim("assets/player_death.png",      frames=5, fps=6, scale=2)
        self.anim      = self.anim_idle

        # Broń
        self.weapons: list[Weapon] = [Weapon.TEARS]      # slot-0
        self.active_slot           = 0                  # używany slot

    # ────────── POMOCNICZE ──────────
    def can_shoot(self) -> bool:
        return self.cool_shot <= 0.0 and not self.dead

    def reset_cooldown(self) -> None:
        weapon = self.weapons[self.active_slot]
        self.cool_shot = WEAPON_CFG[weapon].cooldown

    def hurt(self, dmg: int = 1) -> bool:
        if self.cool_hit > 0.0 or self.dead:
            return False
        self.hp = max(0, self.hp - dmg)
        self.cool_hit = self.COOLDOWN_HIT
        if self.hp == 0:
            self.dead = True
        return True

    def is_dead(self) -> bool:
        return self.dead and self.dead_t >= self.DEATH_TIME

    def select_weapon(self, idx: int):
        """Podświetl slot (0-2) – bez zamiany kolejności."""
        if 0 <= idx < len(self.weapons):
            self.active_slot = idx

    # ────────── ATAK ──────────
    def attack(self, dir_vec: pygame.Vector2, effects, projectiles):
        weapon = self.weapons[self.active_slot]
        stats  = WEAPON_CFG[weapon]

        # TEARS / BOW generują Projectile
        if weapon in (Weapon.TEARS, Weapon.BOW):
            projectiles.append(
                Projectile(
                    self.pos + (14, 8),
                    dir_vec,
                    weapon=weapon,
                    dmg=stats.dmg,
                    speed=stats.speed
                )
            )
        # SWORD = efekt melee
        elif weapon == Weapon.SWORD:
            effects.append(SwordSweep(self, dir_vec, dmg=stats.dmg))

    # ────────── UPDATE ──────────
    def update(self, dt: float) -> None:
        # animacja śmierci
        if self.dead:
            if self.anim_die.index < len(self.anim_die.frames) - 1:
                self.anim_die.update(dt)
            self.dead_t += dt
            return

        # timery
        self.cool_shot = max(0.0, self.cool_shot - dt)
        self.cool_hit  = max(0.0, self.cool_hit  - dt)
        self.slow_t    = max(0.0, self.slow_t    - dt)

        # ruch
        keys    = pygame.key.get_pressed()
        dir_vec = Vector2(keys[pygame.K_d] - keys[pygame.K_a],
                          keys[pygame.K_s] - keys[pygame.K_w])

        if dir_vec.length_squared():
            dir_vec.normalize_ip()
            speed = self.SPEED * (self.SLOW_FACTOR if self.slow_t > 0 else 1.0)
            self.pos += dir_vec * speed * dt
            self.rect.topleft = self.pos

        # animacja
        if not dir_vec.length_squared():
            self.anim = self.anim_idle
        elif abs(dir_vec.x) > abs(dir_vec.y):
            self.anim = self.anim_side
        else:
            self.anim = self.anim_up if dir_vec.y < 0 else self.anim_down

        self.anim.update(dt)

    # ────────── DRAW ──────────
    def draw(self, surf: pygame.Surface, offset: Vector2 = Vector2()) -> None:
        if self.dead:
            img = self.anim_die.image
        else:
            img = self.anim.image
            if self.anim is self.anim_side and (
                pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]
            ):
                img = pygame.transform.flip(img, True, False)

        surf.blit(img, self.rect.move(offset))
