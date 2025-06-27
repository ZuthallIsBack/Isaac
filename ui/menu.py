"""Ekrany menu – start, pauza, przegrana, zwycięstwo."""
from __future__ import annotations
import pygame
from core.gamestate import GameState


class Menu:
    TITLE_SIZE  = 48
    TEXT_SIZE   = 24
    COLOR       = (240, 240, 240)
    SPACING     = 32          # odstęp między wierszami

    def __init__(self, screen: pygame.Surface):
        pygame.font.init()
        self.screen      = screen
        self.font_big    = pygame.font.SysFont("consolas", self.TITLE_SIZE,  bold=True)
        self.font_small  = pygame.font.SysFont("consolas", self.TEXT_SIZE)

    # ------------------------------------------------------------ helpers --
    def _blit_center(self, surf: pygame.Surface, y: int) -> None:
        """Wyrównanie środka na osi X, Y podany piksel (int)."""
        rect = surf.get_rect(midtop=(self.screen.get_width() // 2, y))
        self.screen.blit(surf, rect)

    def _blit_column(self, start_y: int, lines: list[str]) -> None:
        """Lewo-wyrównowana lista – jedna kolumna pod tytułem."""
        anchor_x = self.screen.get_width() // 2 - 120  # kolumna lekko na lewo od środka
        y = start_y
        for line in lines:
            txt = self.font_small.render(line, True, self.COLOR)
            self.screen.blit(txt, (anchor_x, y))
            y += self.SPACING

    # ------------------------------------------------------------- public --
    def draw(self, state: GameState) -> None:
        w, h = self.screen.get_size()

        if state == GameState.MENU_START:
            self._blit_center(self.font_big.render("ISAAC  —  self-made edition", True, self.COLOR),
                              h // 3)

            self._blit_column(
                start_y=h // 2,
                lines=[
                    "[Enter]  start",
                    "[F5]     zapis gry",
                    "[F9]     wczytaj zapis",
                    "[P]      pauza w trakcie gry",
                    "[M]      muzyka on / off",
                    "[Q]      wyjście z gry",
                ],
            )

        elif state == GameState.PAUSED:
            self._blit_center(self.font_big.render("PAUZA", True, self.COLOR), h // 3)
            self._blit_column(
                start_y=h // 2,
                lines=[
                    "[P]    wznów",
                    "[F5]   zapis gry",
                    "[F9]   wczytaj zapis",
                    "[Esc]  menu",
                    "[Q]    wyjście",
                ],
            )

        elif state == GameState.GAME_OVER:
            self._blit_center(self.font_big.render("GAME  OVER", True, self.COLOR), h // 3)
            self._blit_column(
                start_y=h // 2,
                lines=[
                    "[Esc]  menu",
                    "[Q]    wyjście",
                ],
            )

        elif state == GameState.VICTORY:
            self._blit_center(self.font_big.render("VICTORY!", True, self.COLOR), h // 3)
            self._blit_column(
                start_y=h // 2,
                lines=[
                    "[Esc]  menu",
                    "[Q]    wyjście",
                ],
            )
