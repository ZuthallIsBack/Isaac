"""Logika wysokiego poziomu – ekrany, poziom, gracz."""
from __future__ import annotations

import pygame, random
from core.gamestate     import GameState
from core.gameobject    import GameObject
from entities.player    import Player
from entities.enemy     import Slime
from entities.projectile import Projectile
from entities.sword_sweep import SwordSweep
from entities.weapon    import Weapon
from entities.pickup    import Heart
from entities.effects   import Splash, ArrowSplash
from levels.level       import Level
from ui.menu            import Menu
from ui.hud             import HUD
from ui.minimap         import Minimap
from ui.weaponbar       import WeaponBar

_current_game: "Game | None" = None      # używa go SlimeTrail


class Game:
    BG_COLOR = (15, 15, 15)

    # ──────────────────────────── INIT ────────────────────────────
    def __init__(self, screen: pygame.Surface):
        global _current_game
        _current_game = self

        self.screen = screen
        self.state  = GameState.MENU_START
        self.menu   = Menu(screen)
        self.level  = Level()

        # start w centrum siatki 3×3
        center = self.level.rooms[1][1].rect.center
        self.player = Player(center)

        # listy runtime
        self.projectiles: list[Projectile] = []
        self.effects:     list[GameObject] = []
        self.enemies                   = self.level.active_room().enemies

        # UI
        self.hud       = HUD(self.player.MAX_HP)
        self.minimap   = Minimap(self.level)
        self.weaponbar = WeaponBar(self.player)

        # wczytaj pierwszy pokój
        self.level.active_room().enter()
        self.boss_spawned = False

    # ───────────────────── OBSŁUGA ZDARZEŃ ──────────────────────
    def handle_event(self, e: pygame.event.Event) -> None:

        # --- globalne wyjścia ---
        if e.type == pygame.QUIT or (
            e.type == pygame.KEYDOWN and e.key == pygame.K_q
            and self.state in (GameState.MENU_START, GameState.GAME_OVER)
        ):
            pygame.quit(); quit()

        # --- przełączanie stanów ---
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            if self.state == GameState.PLAYING:
                self.state = GameState.PAUSED
            elif self.state == GameState.PAUSED:
                self.state = GameState.PLAYING
            elif self.state == GameState.GAME_OVER:
                self.__init__(self.screen)        # pełny reset

        if (
            e.type == pygame.KEYDOWN
            and e.key == pygame.K_RETURN
            and self.state == GameState.MENU_START
        ):
            self.state = GameState.PLAYING

        # ============ sterowanie, gdy gra trwa ============
        if self.state != GameState.PLAYING:
            return

        # --- atak (strzałki) ---
        if e.type == pygame.KEYDOWN and self.player.can_shoot():
            dir_vec = pygame.Vector2(
                (e.key == pygame.K_RIGHT) - (e.key == pygame.K_LEFT),
                (e.key == pygame.K_DOWN)  - (e.key == pygame.K_UP),
            )
            if dir_vec.length_squared():
                self.player.attack(dir_vec, self.effects, self.projectiles)
                self.player.reset_cooldown()

        # --- wybór broni 1-3 ---
        if e.type == pygame.KEYDOWN and e.key in (pygame.K_1, pygame.K_2, pygame.K_3):
            self.player.select_weapon(e.key - pygame.K_1)

        # --- kółko myszy (rotacja slotów) ---
        if e.type == pygame.MOUSEWHEEL and len(self.player.weapons) > 1:
            nxt = (self.player.active_slot + 1) % len(self.player.weapons)
            self.player.select_weapon(nxt)

    # ───────────────────────── UPDATE ──────────────────────────
    def update(self, dt: float) -> None:
        if self.state != GameState.PLAYING:
            return

        room          = self.level.active_room()
        self.enemies  = room.enemies

        # 0) gracz
        self.player.update(dt)
        if self.player.is_dead():
            self.state = GameState.GAME_OVER
            return
        if not room.doors_open:
            self.player.rect.clamp_ip(room.rect)
            self.player.pos.update(self.player.rect.topleft)

        # ───────── SPAWN BOSS ─────────
        # jeżeli jesteśmy w pokoju (2,2) i jeszcze nie spawnęliśmy:
        if self.level.current == (2, 2) and not self.boss_spawned:
            from entities.beholder import Beholder
            room_center = self.level.active_room().rect.center
            # tworzymy boss na środku pokoju:
            boss = Beholder(room_center)
            self.enemies.append(boss)
            self.boss_spawned = True

        # 1) pociski
        for p in list(self.projectiles):
            p.update(dt)
            if not room.rect.collidepoint(p.pos):
                self.projectiles.remove(p)

        # ─── kolizja: pocisk → gracz ───
        for p in list(self.projectiles):
            if p.owner is not self.player and p.rect.colliderect(self.player.rect):
                self.player.hurt(p.dmg)
                self.projectiles.remove(p)

        # 2) wrogowie
        for e in list(self.enemies):

            if getattr(e, "dying", False):       # odtwarzanie śmierci
                e.update(dt, self.player.pos)
                continue

            e.update(dt, self.player.pos)

            # 2a) pocisk → wróg
            for p in list(self.projectiles):
                if p.owner is e:
                    continue
                if e.rect.colliderect(p.rect):
                    self.projectiles.remove(p)
                    eff_cls = ArrowSplash if p.weapon == Weapon.BOW else Splash
                    self.effects.append(eff_cls(p.pos))
                    e.take_damage(p.dmg)
                    break

            # 2b) sword sweep → wróg
            for eff in self.effects:
                if isinstance(eff, SwordSweep) and eff.rect.colliderect(e.rect):
                    e.take_damage(eff.dmg)

            # 2c) wróg → gracz
            if e.rect.colliderect(self.player.rect):
                if isinstance(e, Slime):
                    self.player.slow_t = self.player.SLOW_DURATION
                self.player.hurt(1)

        # usuń wrogów po zakończeniu anim. śmierci
        for e in list(self.enemies):
            if e.is_dead():
                self.enemies.remove(e)

        # 3) efekty
        for eff in list(self.effects):
            eff.update(dt)
            if getattr(eff, "SLOW", False) and eff.rect.colliderect(self.player.rect):
                self.player.slow_t = self.player.SLOW_DURATION
            if getattr(eff, "done", False):
                self.effects.remove(eff)

        # 4) pick-upy
        for item in list(room.pickups):
            if isinstance(item, Heart):
                if (
                    item.rect.colliderect(self.player.rect)
                    and self.player.hp < self.player.MAX_HP
                ):
                    self.player.hp += 1
                    room.pickups.remove(item)
            elif hasattr(item, "open"):          # Chest
                if item.rect.colliderect(self.player.rect):
                    item.open(self.player)
                    room.pickups.remove(item)

            if hasattr(item, "update"):
                item.update(dt)

        # 5) logika poziomu
        self.level.update(self.player)

    # ───────────────────────── DRAW ────────────────────────────
    def draw(self) -> None:
        self.screen.fill(self.BG_COLOR)

        if self.state in (GameState.PLAYING, GameState.PAUSED):
            # 0) tło
            self.level.draw(self.screen)
            offset = self.level.world_offset()

            # 1) SlimeTrail
            for eff in self.effects:
                if getattr(eff, "SLOW", False):
                    eff.draw(self.screen, offset)

            # 2) pociski
            for proj in self.projectiles:
                proj.draw(self.screen, offset)

            # 3a) wrogowie żywi
            for enemy in self.enemies:
                if not getattr(enemy, "dying", False):
                    enemy.draw(self.screen, offset)

            # 3b) pick-upy
            for item in self.level.active_room().pickups:
                item.draw(self.screen, offset)

            # 3c) wrogowie dying
            for enemy in self.enemies:
                if getattr(enemy, "dying", False):
                    enemy.draw(self.screen, offset)

            # 3d) efekty trafienia (bez SwordSweep)
            for eff in self.effects:
                if not getattr(eff, "SLOW", False) and not isinstance(eff, SwordSweep):
                    eff.draw(self.screen, offset)

            # 4) gracz
            if not self.player.dead:
                self.player.draw(self.screen, offset)

            # 4a) SwordSweep
            for eff in self.effects:
                if isinstance(eff, SwordSweep):
                    eff.draw(self.screen, offset)

            # 5) HUD + minimapa + pasek broni
            self.hud.draw(self.screen, self.player.hp)
            self.minimap.draw(self.screen)
            self.weaponbar.draw(self.screen)

            # 6) animacja śmierci gracza
            if self.player.dead:
                self.player.draw(self.screen, offset)

        if self.state in (GameState.MENU_START, GameState.PAUSED, GameState.GAME_OVER):
            self.menu.draw(self.state)
