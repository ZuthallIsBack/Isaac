# entities/chest.py
import random, pygame

from core.gameobject import GameObject
from entities.weapon import Weapon

class Chest(GameObject):
    SIZE = (32, 32)

    # tylko przydatne bronie – bez TEARS
    WEAPON_POOL = (Weapon.BOW, Weapon.SWORD)

    def __init__(self, pos):
        super().__init__(pos, self.SIZE)

        # grafika
        img = pygame.image.load("assets/chest.png").convert_alpha()
        self.img = pygame.transform.scale2x(img)

        # stan
        self.opened = False

    # ────────────────────────────────────────────────────────────────
    def open(self, player):
        """Otwórz skrzynię:
        – jeśli gracz ma już łzy, wypadnie łuk lub miecz,
        – jeśli ma miecz → wypadnie łuk,
        – jeśli ma łuk → wypadnie miecz,
        – nigdy nie dostanie duplikatu ani TEARS."""
        if self.opened:
            return
        self.opened = True

        # lista broni, których gracz wciąż nie ma
        candidates = [w for w in self.WEAPON_POOL if w not in player.weapons]

        if candidates and len(player.weapons) < 3:
            weapon_inside = random.choice(candidates)
            player.weapons.append(weapon_inside)
        # jeśli `candidates` puste (gracz ma już obu), skrzynia nic nie daje

    # ────────────────────────────────────────────────────────────────
    def update(self, dt: float):
        pass  # statyczny obiekt

    def draw(self, surf, offset=pygame.Vector2()):
        surf.blit(self.img, self.rect.move(offset))
