import pygame
from entities.weapon import Weapon


class WeaponBar:
    """Trzyslotowy pasek broni z podświetleniem aktywnej."""
    SLOT   = 24
    PAD    = 6
    BG_CLR = (0, 0, 0, 160)

    _ICONS: dict[Weapon | str, pygame.Surface] = {}
    _FONT:  pygame.font.Font | None = None

    def __init__(self, player):
        self.player = player

        # ── lazy-load czcionki (po pygame.init()) ──
        if WeaponBar._FONT is None:
            if not pygame.font.get_init():
                pygame.font.init()
            WeaponBar._FONT = pygame.font.SysFont("arial", 14)

        # ── lazy-load ikonek ──
        if not WeaponBar._ICONS:
            WeaponBar._ICONS = {
                Weapon.TEARS: pygame.image.load("assets/weapon_icons/tear.png").convert_alpha(),
                Weapon.BOW:   pygame.image.load("assets/weapon_icons/bow.png").convert_alpha(),
                Weapon.SWORD: pygame.image.load("assets/weapon_icons/sword.png").convert_alpha(),
                "empty":      pygame.image.load("assets/weapon_icons/slot_empty.png").convert_alpha()
            }

    # ─────────────────────────── DRAW ───────────────────────────
    def draw(self, surf: pygame.Surface):
        ww, wh = surf.get_size()
        bar_w  = self.SLOT * 3 + self.PAD * 4
        bar_h  = self.SLOT     + self.PAD * 2
        bar_xy = (ww // 2 - bar_w // 2, wh - bar_h - 8)

        # pół-przezroczyste tło
        bg = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)
        bg.fill(self.BG_CLR)
        surf.blit(bg, bar_xy)

        # ───── LISTA BRONI ─────
        #   nowy system: player.weapons (lista slotów)
        weapons = self.player.weapons[:3]            # max 3 sloty
        weapons += ["empty"] * (3 - len(weapons))    # dopełnij pustymi

        for i, wpn in enumerate(weapons):
            x = bar_xy[0] + self.PAD + i * (self.SLOT + self.PAD)
            y = bar_xy[1] + self.PAD

            # ramka: złota gdy slot == active_slot
            is_active = (i == self.player.active_slot)
            clr = (255, 215, 64) if is_active else (200, 200, 200)
            rect = pygame.Rect(x-1, y-1, self.SLOT+2, self.SLOT+2)
            pygame.draw.rect(surf, clr, rect, width=2, border_radius=4)

            # ikonka
            icon = pygame.transform.smoothscale(self._ICONS[wpn], (self.SLOT, self.SLOT))
            surf.blit(icon, (x, y))

            # numer klawisza 1-3
            num = WeaponBar._FONT.render(str(i+1), True, clr)
            surf.blit(num, (x + self.SLOT - 8, y + self.SLOT - 14))
