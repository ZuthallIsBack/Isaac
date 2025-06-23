"""Logika wysokiego poziomu – ekrany, poziom, gracz."""
import pygame
from core.gamestate import GameState
from entities.player import Player
from levels.level import Level
from ui.menu import Menu
from entities.projectile import Projectile
from entities.enemy import Charger
from ui.hud import HUD


class Game:
    BG_COLOR = (15, 15, 15)

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.state = GameState.MENU_START
        self.menu = Menu(screen)
        self.level = Level()

        center_room = self.level.rooms[1][1]

        # pozycja „światowa” = offset pokoju + środek pokoju
        start_world = (
            center_room.grid_x * center_room.SIZE[0] + center_room.rect.centerx,
            center_room.grid_y * center_room.SIZE[1] + center_room.rect.centery,
        )
        self.player = Player(start_world)
        # ───────── Sprint 2 lists ─────────
        self.projectiles: list[Projectile] = []
        self.enemies: list[Charger] = [Charger(self.player.pos + pygame.Vector2(120, 0))]
        self.hud = HUD(self.player.MAX_HP)

    # ──────────────────────────────────────────────────────────── EVENTY ─────
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if self.state == GameState.MENU_START and event.key == pygame.K_RETURN:
                self.state = GameState.PLAYING
            elif self.state == GameState.PLAYING and event.key == pygame.K_ESCAPE:
                self.state = GameState.PAUSED
            elif self.state == GameState.PAUSED and event.key == pygame.K_ESCAPE:
                self.state = GameState.PLAYING

        if self.state == GameState.PLAYING:
            self.player.handle_event(event)

        # strzał kierunkowy (strzałki)
        if event.type == pygame.KEYDOWN and self.player.can_shoot():
            dir_vec = pygame.Vector2(0, 0)
            if event.key == pygame.K_UP:
                dir_vec.y = -1
            elif event.key == pygame.K_DOWN:
                dir_vec.y = 1
            elif event.key == pygame.K_LEFT:
                dir_vec.x = -1
            elif event.key == pygame.K_RIGHT:
                dir_vec.x = 1
            if dir_vec.length_squared():          # faktycznie wcisnięto strzałkę
                self.projectiles.append(Projectile(self.player.pos, dir_vec))
                self.player.reset_cooldown()


    # ─────────────────────────────────────────────────────────── UPDATE ─────
    def update(self, dt: float) -> None:
        if self.state == GameState.PLAYING:
            self.player.update(dt)
            # ───────── pociski ─────────
            for proj in list(self.projectiles):
                proj.update(dt)
                # usuń, jeśli wyszedł poza aktywny pokój
                if not self.level.active_room().rect.collidepoint(proj.pos):
                    self.projectiles.remove(proj)

            # ───────── wrogowie ────────
            for enemy in list(self.enemies):
                enemy.update(dt, self.player.pos)

                # trafienie pociskiem
                for proj in list(self.projectiles):
                    if enemy.rect.colliderect(proj.rect):
                        self.projectiles.remove(proj)
                        if enemy.take_damage(1):
                            self.enemies.remove(enemy)
                        break

                # kolizja wróg–gracz
                if enemy.rect.colliderect(self.player.rect):
                    self.player.hp = max(0, self.player.hp - 1)

            self.level.update(self.player)  # ← przekazujemy obiekt Player

    # ───────────────────────────────────────────────────────────── DRAW ─────
    def draw(self) -> None:
        self.screen.fill(self.BG_COLOR)
        if self.state in (GameState.PLAYING, GameState.PAUSED):
            self.level.draw(self.screen)
            # offset ekranu – gracza rysujemy po transformacji
            offset = self.level.world_offset()
            self.player.draw(self.screen, offset)
            for proj in self.projectiles:
                proj.draw(self.screen, offset)
            for enemy in self.enemies:
                enemy.draw(self.screen, offset)
            self.hud.draw(self.screen, self.player.hp)

        if self.state in (GameState.MENU_START, GameState.PAUSED):
            self.menu.draw(self.state)