"""Logika wysokiego poziomu – ekrany, poziom, gracz."""
import pygame
from core.gamestate import GameState
from entities.player import Player
from levels.level import Level
from ui.menu import Menu


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

    # ─────────────────────────────────────────────────────────── UPDATE ─────
    def update(self, dt: float) -> None:
        if self.state == GameState.PLAYING:
            self.player.update(dt)
            self.level.update(self.player)  # ← przekazujemy obiekt Player

    # ───────────────────────────────────────────────────────────── DRAW ─────
    def draw(self) -> None:
        self.screen.fill(self.BG_COLOR)
        if self.state in (GameState.PLAYING, GameState.PAUSED):
            self.level.draw(self.screen)
            # offset ekranu – gracza rysujemy po transformacji
            offset = self.level.world_offset()
            self.player.draw(self.screen, offset)
        if self.state in (GameState.MENU_START, GameState.PAUSED):
            self.menu.draw(self.state)