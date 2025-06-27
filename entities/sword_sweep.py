# sword_sweep.py
import math, pygame
from core.gameobject import GameObject
from utils.anim import SpriteAnim


class SwordSweep(GameObject):
    LIFE = 0.25            # sekund

    def __init__(self, player, dir_vec: pygame.Vector2, dmg: int = 2):
        if not hasattr(SwordSweep, "_ANIM"):
            SwordSweep._ANIM = SpriteAnim(
                "assets/sword_sweep.png", frames=8, fps=30, scale=2
            )

        # inicjalny rect – rozmiar jednej klatki po skali
        w, h = SwordSweep._ANIM.image.get_size()
        super().__init__((0, 0), (w, h))

        self.player  = player
        self.dir_vec = dir_vec.normalize()
        self.dmg     = dmg
        self.timer   = 0.0
        self.angle_deg = -math.degrees(math.atan2(self.dir_vec.y, self.dir_vec.x))

        self._refresh_image()   # tworzy self.image i self.rect
        self._sync_position()   # ustawia rect.center względem gracza

    # ------------------------------------------------------------------
    def _refresh_image(self):
        """Weź bieżącą klatkę animacji, obróć i nadaj **NOWY** rect."""
        frame = SwordSweep._ANIM.image
        self.image = pygame.transform.rotate(frame, self.angle_deg)
        self.rect  = self.image.get_rect()          # pełny bounding-box

    def _sync_position(self):
        """Ustaw środek animacji na środku gracza, wysunięty o 8 px."""
        offset = self.dir_vec * 8
        self.rect.center = (
            self.player.rect.centerx + offset.x,
            self.player.rect.centery + offset.y,
        )

    # ------------------------------------------------------------------
    def update(self, dt: float):
        self.timer += dt
        SwordSweep._ANIM.update(dt)

        self._refresh_image()   # obrót + nowy rect
        self._sync_position()   # i dopiero potem ustawienie pozycji

    @property
    def done(self):
        return self.timer >= self.LIFE

    def draw(self, surf: pygame.Surface, offset=pygame.Vector2()):
        surf.blit(self.image, self.rect.move(offset))
