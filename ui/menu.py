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
            title = self.font_big.render("Isaac‑Clone", True, self.COLOR)
            prompt = self.font_small.render("[Enter] start", True, self.COLOR)
            quit_txt = self.font_small.render("[Q] wyjście", True, self.COLOR)
            self.screen.blit(quit_txt, quit_txt.get_rect(center=(w // 2, h // 1.45)))
            self.screen.blit(title, title.get_rect(center=(w // 2, h // 3)))
            self.screen.blit(prompt, prompt.get_rect(center=(w // 2, h // 1.6)))
        elif state == GameState.PAUSED:
            pause = self.font_big.render("PAUSED", True, self.COLOR)
            prompt = self.font_small.render("[Esc] wróć", True, self.COLOR)
            self.screen.blit(pause, pause.get_rect(center=(w // 2, h // 2.5)))
            self.screen.blit(prompt, prompt.get_rect(center=(w // 2, h // 1.8)))
        elif state == GameState.GAME_OVER:
            over = self.font_big.render("GAME OVER", True, self.COLOR)
            prompt = self.font_small.render("[Esc] menu", True, self.COLOR)
            prompt_quit = self.font_small.render("[Q] wyjście", True, self.COLOR)
            self.screen.blit(prompt_quit, prompt_quit.get_rect(center=(w // 2, h // 1.6)))
            self.screen.blit(over, over.get_rect(center=(w // 2, h // 2.5)))
            self.screen.blit(prompt, prompt.get_rect(center=(w // 2, h // 1.8)))
        elif state == GameState.VICTORY:
            victory = self.font_big.render("VICTORY", True, self.COLOR)
            prompt = self.font_small.render("[Esc] menu", True, self.COLOR)
            prompt_quit = self.font_small.render("[Q] wyjście", True, self.COLOR)
            self.screen.blit(victory, prompt.get_rect(center=(w // 2, h // 1.6)))
            self.screen.blit(prompt, prompt.get_rect(center=(w // 2, h // 2.5)))
            self.screen.blit(prompt_quit, prompt_quit.get_rect(center=(w // 2, h // 1.8)))