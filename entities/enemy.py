import random

import pygame
from core.gameobject import MovingObject
from utils.anim import SpriteAnim
from entities.effects import SlimeTrail

class Bat(MovingObject):
    SIZE = (32, 16)
    # COLOR = (200, 60, 60)
    SPEED = 120
    MAX_HP = 3
    DEATH_TIME = 1

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, self.SIZE)
        self.hp = self.MAX_HP
        self.anim_walk = SpriteAnim("assets/bat_walk.png", frames=3, fps=10, scale=2)
        self.anim_idle = SpriteAnim("assets/bat_idle.png", frames=1, scale=2)
        self.anim_die = SpriteAnim("assets/bat_death.png", frames=5, fps=7, scale=2)
        self.dying = False
        self.dead_timer = 0.0

    def take_damage(self, dmg=1) -> None:
        if self.dying:
            return
        self.hp -= dmg
        if self.hp <= 0:
            self.dying = True

    def is_dead(self) -> bool:
        return self.dying and self.dead_timer >= self.DEATH_TIME

    def update(self, dt: float, target_pos: pygame.Vector2) -> None:
        if self.dying:
            if self.anim_die.index < len(self.anim_die.frames) - 1:
                self.anim_die.update(dt)
            self.dead_timer += dt
            return
        direction = target_pos - self.pos
        if direction.length_squared() > 0:
            self.pos += direction.normalize() * self.SPEED * dt
            self.rect.topleft = self.pos
        self.anim_walk.update(dt)


    def draw(self, surface: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2()) -> None:
        if self.dying:
            img = self.anim_die.image
        else:
            img = self.anim_walk.image
        surface.blit(img, self.rect.move(offset))

class Slime(MovingObject):
    SIZE   = (32, 32)          # collider ~ sprite
    SPEED  = 80                # wolniejszy od nietoperza
    MAX_HP = 4
    SLOW = True
    DEATH_TIME = 3

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, self.SIZE)
        self.trail_cd = 0.0
        self.hp = self.MAX_HP
        self.anim = SpriteAnim("assets/slime_walk.png", frames=5, fps=8, scale=2)
        self.move_dir = pygame.Vector2()  # bieżący kierunek ruchu
        self.dir_timer = 0.75  # czas do kolejnej zmiany (sekundy)
        self.DIR_PERIOD = 0.5  # losujemy wektor co 0.5 s
        self.anim_die = SpriteAnim("assets/slime_death.png", frames=5, fps=2, scale=2)
        self.dying = False
        self.dead_timer = 0.0

    def take_damage(self, dmg=1) -> None:
        if self.dying:
            return
        self.hp -= dmg
        if self.hp <= 0:
            self.dying = True

    def update(self, dt: float, target_pos: pygame.Vector2) -> None:
        # --- losuj nowy kierunek co DIR_PERIOD ---
        self.dir_timer -= dt
        if self.dir_timer <= 0:
            self.dir_timer = self.DIR_PERIOD

            if random.random() < 0.7:  # 70 % bias na gracza
                self.move_dir = (target_pos - self.pos).normalize() if (
                                                                                   target_pos - self.pos).length_squared() > 0 else pygame.Vector2()
            else:  # 30 % czysto losowy bok
                angles = [pygame.Vector2(1, 0), pygame.Vector2(-1, 0),
                          pygame.Vector2(0, 1), pygame.Vector2(0, -1)]
                self.move_dir = random.choice(angles)
        if self.dying:
            # odtwarzaj tylko do ostatniej klatki
            if self.anim_die.index < len(self.anim_die.frames) - 1:
                self.anim_die.update(dt)
            self.dead_timer += dt
            return

        # --- przesuń Slim’a ---
        self.pos += self.move_dir * self.SPEED * dt
        self.rect.topleft = self.pos

        # --- animacja + trail jak wcześniej ---
        self.anim.update(dt)

        self.trail_cd -= dt
        if self.trail_cd <= 0:
            self.trail_cd = 0.2
            from core import game
            game._current_game.effects.append(SlimeTrail(self.rect.topleft))

    def draw(self, surf: pygame.Surface, offset=pygame.Vector2()) -> None:
        img = self.anim_die.image if self.dying else self.anim.image
        surf.blit(img, self.rect.move(offset))


    def is_dead(self) -> bool:
        return self.dying and self.dead_timer >= self.DEATH_TIME
