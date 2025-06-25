"""Implementacja sterowanej przez użytkownika postaci."""
import pygame
from core.gameobject import MovingObject
from utils.anim import SpriteAnim

class Player(MovingObject):
    SPEED = 200  # piksele na sekundę
    # COLOR = (180, 180, 255)
    SIZE = (32, 32)
    MAX_HP = 3
    COOLDOWN = 0.25  # s
    HIT_COOLDOWN = 1.0
    SLOW_FACTOR = 0.5
    SLOW_DURATION = 1.0

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, self.SIZE)
        self.cooldown = 0.0
        self.hp = self.MAX_HP
        self.hit_cd = 0.0  # timer invincibility
        self.anim_idle = SpriteAnim("assets/player_idle.png", frames=1, scale=2)
        self.anim_walk = SpriteAnim("assets/player_walk.png", frames=3, scale=2)
        self.anim_up = SpriteAnim("assets/player_walk_up.png", frames=3, scale=2)
        self.anim_down = SpriteAnim("assets/player_walk_down.png", frames=3, scale=2)
        self.current_anim = self.anim_idle
        self.anim_die = SpriteAnim("assets/player_death.png", frames=5, fps=6, scale=2)
        self.dead = False
        self.dead_timer = 0.0
        self.slow_timer = 0.0

    # ───────── shooting helpers ──────────────────────────
    def can_shoot(self) -> bool:
        return self.cooldown <= 0.0

    def reset_cooldown(self) -> None:
        self.cooldown = self.COOLDOWN

    # ───────── damage helper ─────────────────────────
    def hurt(self, dmg: int = 1) -> bool:
        """Zwraca True, jeśli faktycznie odebrano życie."""
        if self.hp == 0:
            self.dead = True
        if self.hit_cd <= 0.0 and self.hp > 0:
            self.hp = max(0, self.hp - dmg)
            self.hit_cd = self.HIT_COOLDOWN
            return True
        return False

    def is_dead(self) -> bool:
        return self.dead and self.dead_timer >= 1.5  # 0.5 s animacji

    # ──────────────────────────────────────────────────────────── API ────────
    def handle_event(self, event: pygame.event.Event) -> None:
        """Na razie nic nie robi – sterowanie zbieramy w update()."""
        pass

    def update(self, dt: float) -> None:
        if self.dead:
            # aktualizuj, dopóki nie osiągniesz ostatniej klatki
            if self.anim_die.index < len(self.anim_die.frames) - 1:
                self.anim_die.update(dt)
            self.dead_timer += dt
            return
        self.slow_timer = max(0.0, self.slow_timer - dt)
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
            speed = self.SPEED * (self.SLOW_FACTOR if self.slow_timer > 0 else 1.0)
            self.pos += direction * speed * dt
            self.rect.topleft = self.pos

        moving = direction.length_squared() > 0
        if moving:
            # w którą oś porusza się bardziej?
            if abs(direction.x) > abs(direction.y):
                self.current_anim = self.anim_walk  # HORYZONTALNIE
            else:
                self.current_anim = self.anim_up if direction.y < 0 else self.anim_down
        else:
            self.current_anim = self.anim_idle

        self.current_anim.update(dt)

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2()) -> None:
        if self.dead:
            surface.blit(self.anim_die.image, self.rect.move(offset))
            return
        img = self.current_anim.image
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # idziemy w prawo
            img = pygame.transform.flip(img, True, False)  # poziome odbicie
        surface.blit(img, self.rect.move(offset))

