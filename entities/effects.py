import pygame
from utils.anim import SpriteAnim
from core.gameobject import GameObject


class Splash(GameObject):
    """Krótka animacja trafienia łzy w coś."""

    def __init__(self, pos: tuple[int, int]):
        # ── ZAŁADUJ arkusz tylko przy pierwszej instancji ──
        if not hasattr(Splash, "ANIM"):
            Splash.ANIM = SpriteAnim("assets/tear_splash.png", frames=2, fps=15, scale=2)
        super().__init__(pos, (Splash.ANIM.image.get_width(), Splash.ANIM.image.get_height()))
        self.timer = 0.0
        self.done  = False

    def update(self, dt: float) -> None:
        Splash.ANIM.update(dt)
        self.timer += dt
        if self.timer >= 0.13:
            self.done = True

    def draw(self, surf: pygame.Surface, offset=pygame.Vector2()) -> None:
        surf.blit(Splash.ANIM.image, self.rect.move(offset))

class SlimeTrail(GameObject):
    """4-klatkowa animacja śluzu, zanika po 6 s i spowalnia gracza."""
    SLOW = True                 # ← znacznik: plama daje slow

    def __init__(self, topleft: pygame.Vector2):     # zmieniamy nazwę arg.
        if not hasattr(SlimeTrail, "_ANIM"):
            SlimeTrail._ANIM = SpriteAnim(
                "assets/slime_trail.png", frames=4, fps=1, scale=2
            )
        w, h = SlimeTrail._ANIM.image.get_size()
        super().__init__(topleft, (w, h))            # używamy dokładnego topleft
        self.timer = 0.0
        self.life  = 6.0

    def update(self, dt: float) -> None:
        self.timer += dt
        SlimeTrail._ANIM.update(dt)

    def draw(self, surf: pygame.Surface, offset=pygame.Vector2()) -> None:
        fade = max(0, 1 - self.timer / self.life)
        img  = SlimeTrail._ANIM.image.copy()
        img.set_alpha(int(255 * fade))
        surf.blit(img, self.rect.move(offset))

    @property
    def done(self) -> bool:
        return self.timer >= self.life

class ArrowSplash(GameObject):
    """Animacja trafienia strzałą."""
    def __init__(self, pos: tuple[int, int]):
        if not hasattr(ArrowSplash, "ANIM"):
            ArrowSplash.ANIM = SpriteAnim(
                "assets/arrow_splash.png",   # ← dodaj własny sprite-sheet
                frames=2, fps=15, scale=2
            )
        super().__init__(pos, ArrowSplash.ANIM.image.get_size())
        self.timer = 0.0
        self.done  = False

    def update(self, dt: float) -> None:
        ArrowSplash.ANIM.update(dt)
        self.timer += dt
        if self.timer >= 0.15:               # ~3 klatki przy 18 fps
            self.done = True

    def draw(self, surf, offset=pygame.Vector2()) -> None:
        surf.blit(ArrowSplash.ANIM.image, self.rect.move(offset))
