import math, pygame
from core.gameobject import GameObject
from utils.anim import SpriteAnim

class SwordSweep(GameObject):
    LIFE = 0.25   # s

    def __init__(
        self,
        player,                       # ← referencja do obiektu Player
        dir_vec: pygame.Vector2,
        dmg: int = 2
    ):
        if not hasattr(SwordSweep, "_ANIM"):
            SwordSweep._ANIM = SpriteAnim(
                "assets/sword_sweep.png", frames=8, fps=30, scale=2
            )

        # rozmiar pojedynczej (przeskalowanej) klatki
        w, h = SwordSweep._ANIM.image.get_size()
        super().__init__((0, 0), (w, h))     # pozycję ustawimy w update()

        self.player    = player
        self.dir_vec   = dir_vec.normalize()
        self.dmg       = dmg
        self.timer     = 0.0
        self.angle_deg = -math.degrees(math.atan2(self.dir_vec.y, self.dir_vec.x))

        self._refresh_image()
        self._sync_position()                # pierwsze ustawienie

    # ---------- pomocnicy ----------
    def _refresh_image(self):
        frame = SwordSweep._ANIM.image
        self.image = pygame.transform.rotate(frame, self.angle_deg)

    def _sync_position(self):
        """Trzymaj rect środka animacji na środku gracza,
        lekko wysunięty w kierunku zamachu (8 px)."""
        offset = self.dir_vec * 8
        self.rect.center = (self.player.rect.centerx + offset.x,
                            self.player.rect.centery + offset.y)

    # ---------- API ----------
    def update(self, dt: float):
        self.timer += dt
        SwordSweep._ANIM.update(dt)
        self._refresh_image()     # nowa klatka → odśwież obrót
        self._sync_position()     # podążaj za graczem

    @property
    def done(self):
        return self.timer >= self.LIFE

    def draw(self, surf, offset=pygame.Vector2()):
        surf.blit(self.image, self.rect.move(offset))
