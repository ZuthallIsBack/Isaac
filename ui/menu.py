"""Prosty ekran menu – start i pauza."""
import pygame
from core.gamestate import GameState

class Menu:
    FONT_SIZE = 48
    SMALL_SIZE = 24
    COLOR = (240, 240, 240)

    def __init__(self, screen: pygame.Surface):
        pygame.font.init()
        self.screen = screen
        self.font_big = pygame.font.SysFont("consolas", self.FONT_SIZE, bold=True)
        self.font_small = pygame.font.SysFont("consolas", self.SMALL_SIZE)

    # ──────────────────────────────────────────────────────────── API ────────
    def draw(self, state: GameState) -> None:
        w, h = self.screen.get_size()
        if state == GameState.MENU_START:
            w, h = self.screen.get_size()

            title = self.font_big.render("ISAAC - selfmade version", True, self.COLOR)
            self.screen.blit(title, title.get_rect(center=(w // 2, h // 3)))

            # lewa krawędź listy (-100 px od środka)
            anchor_x = w // 2 - 100
            y = h // 2
            for line in (
                    "[Enter]  start",
                    "[F5]     zapis gry",
                    "[F9]     wczytaj zapis",
                    "[P]      pauza w trakcie gry",
                    "[M]      muzyka on / off",
                    "[Q]      wyjście z gry",
            ):
                txt = self.font_small.render(line, True, self.COLOR)
                self.screen.blit(txt, (anchor_x, y))  # ← wyrównanie do lewej
                y += 32

        elif state == GameState.PAUSED:
            w, h = self.screen.get_size()
            pause = self.font_big.render("PAUZA", True, self.COLOR)
            unp = self.font_small.render("[P] wznów", True, self.COLOR)
            quit_ = self.font_small.render("[Q] wyjście", True, self.COLOR)

            self.screen.blit(pause, pause.get_rect(center=(w // 2, h // 3)))
            self.screen.blit(unp, unp.get_rect(center=(w // 2, h // 1.8)))
            self.screen.blit(quit_, quit_.get_rect(center=(w // 2, h // 1.6)))

        elif state == GameState.GAME_OVER:
            w, h = self.screen.get_size()
            over = self.font_big.render("GAME OVER", True, self.COLOR)
            esc = self.font_small.render("[Esc]  menu", True, self.COLOR)
            quit_ = self.font_small.render("[Q]    wyjście", True, self.COLOR)

            self.screen.blit(over, over.get_rect(center=(w // 2, h // 3)))
            self.screen.blit(esc, esc.get_rect(center=(w // 2, h // 1.8)))
            self.screen.blit(quit_, quit_.get_rect(center=(w // 2, h // 1.6)))

        elif state == GameState.VICTORY:
            w, h = self.screen.get_size()
            win = self.font_big.render("VICTORY!", True, self.COLOR)
            esc = self.font_small.render("[Esc]  menu", True, self.COLOR)
            quit_ = self.font_small.render("[Q]    wyjście", True, self.COLOR)

            self.screen.blit(win, win.get_rect(center=(w // 2, h // 3)))
            self.screen.blit(esc, esc.get_rect(center=(w // 2, h // 1.8)))
            self.screen.blit(quit_, quit_.get_rect(center=(w // 2, h // 1.6)))

