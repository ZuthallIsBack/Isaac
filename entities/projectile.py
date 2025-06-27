# entities/projectile.py
import math, pygame
from core.gameobject import MovingObject
from entities.weapon import Weapon

class Projectile(MovingObject):
    SIZE  = (8, 8)
    SPEED = 450

    def __init__(
        self,
        pos: tuple[int, int],
        direction: pygame.Vector2,
        *,
        weapon: Weapon | None = None,
        dmg: int = 1,
        speed: float | None = None,
        owner: object | None = None,
    ):
        from entities.weapon import Weapon as _W
        weapon = weapon or _W.TEARS

        # Ładowanie grafik (raz, globalnie)
        if not hasattr(Projectile, "IMG_TEAR"):
            Projectile.IMG_TEAR  = pygame.image.load("assets/tear.png").convert_alpha()
            Projectile.IMG_ARROW = pygame.image.load("assets/arrow.png").convert_alpha()

        super().__init__(pos, self.SIZE)

        # Sprite bazowy
        base_img = Projectile.IMG_ARROW if weapon == _W.BOW else Projectile.IMG_TEAR

        # Jeśli strzela Beholder → fioletowy duplikat łzy
        if owner and owner.__class__.__name__ == "Beholder":
            base_img = Projectile.IMG_TEAR.copy()
            base_img.fill((255, 60, 60, 255), special_flags=pygame.BLEND_RGBA_MULT)

        # Obrót
        self.direction = pygame.Vector2(direction).normalize()
        angle_deg      = -math.degrees(math.atan2(self.direction.y, self.direction.x))
        self.image_rot = pygame.transform.rotate(base_img, angle_deg)
        self.rect      = self.image_rot.get_rect(center=self.pos)

        # Atrybuty logiki
        self.weapon = weapon
        self.owner  = owner
        self.dmg    = dmg
        self.speed  = speed or self.SPEED

    # -------------------- MUSI BYĆ NA TYM SAMYM WCIĘCIU CO __init__ ------
    def update(self, dt: float) -> None:
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = self.pos

    def draw(self, surf: pygame.Surface, offset=pygame.Vector2()) -> None:
        surf.blit(self.image_rot, self.rect.move(offset))
