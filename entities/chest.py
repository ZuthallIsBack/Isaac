import random, pygame
from core.gameobject import GameObject
from entities.weapon import Weapon


class Chest(GameObject):
    SIZE = (32, 32)

    def __init__(self, pos):
        super().__init__(pos, self.SIZE)

        # grafika
        img = pygame.image.load("assets/chest.png").convert_alpha()
        self.img = pygame.transform.scale2x(img)

        # stan
        self.opened = False
        self.weapon_inside: Weapon = random.choice(list(Weapon))

    # ──────────────────────────────────────────────────────────────────
    def open(self, player):
        """Dodaj broń do pierwszego wolnego slotu gracza (max 3)."""
        if self.opened:
            return
        self.opened = True

        # unik dubli i limit 3 slotów
        if (
            self.weapon_inside not in player.weapons
            and len(player.weapons) < 3
        ):
            player.weapons.append(self.weapon_inside)

    # ──────────────────────────────────────────────────────────────────
    def update(self, dt: float):
        """Statyczny obiekt – brak logiki czasowej."""
        pass

    def draw(self, surf, offset=pygame.Vector2()):
        surf.blit(self.img, self.rect.move(offset))
