"""Logika wysokiego poziomu – zarządza sceną i aktualizacjami."""
import pygame
from entities.player import Player


class Game:
    """Kontener na stan gry."""

    BG_COLOR = (20, 20, 20)

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        # Umieszczamy gracza na środku ekranu
        center = (screen.get_width() // 2, screen.get_height() // 2)
        self.player = Player(center)

    # ────────────────────────────────────────────────────────── PUBLIC API ─────
    def handle_event(self, event: pygame.event.Event) -> None:
        """Przekazuje zdarzenie do obiektów gry."""
        self.player.handle_event(event)

    def update(self, dt: float) -> None:
        """Aktualizuje wszystkie obiekty."""
        self.player.update(dt)

    def draw(self) -> None:
        """Renderuje scenę na ekranie."""
        self.screen.fill(self.BG_COLOR)
        self.player.draw(self.screen)