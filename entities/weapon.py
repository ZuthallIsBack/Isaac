from enum import Enum, auto
from dataclasses import dataclass

class Weapon(Enum):
    TEARS = auto()
    BOW = auto()
    SWORD = auto()

# ───────── parametry każdej broni ─────────
@dataclass(frozen=True)
class WeaponStats:
    dmg:       int        # obrażenia pojedynczego trafienia
    cooldown:  float      # czas między atakami (s)
    speed:     int = 0    # prędkość pocisku (0 = brak)

WEAPON_CFG: dict[Weapon, WeaponStats] = {
    Weapon.TEARS: WeaponStats(dmg=1, cooldown=0.25, speed=450),
    Weapon.BOW:   WeaponStats(dmg=2, cooldown=0.35, speed=550),
    Weapon.SWORD: WeaponStats(dmg=2, cooldown=0.15)              # speed=0 ⇒ melee
}