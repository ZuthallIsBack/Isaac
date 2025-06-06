"""Główne uruchomienie gry."""
import pygame
from core.game import Game


def main() -> None:
    pygame.init()
    pygame.mixer.init()

    WIDTH, HEIGHT = 960, 540
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Isaac Clone – sprint 1 prototype")

    clock = pygame.time.Clock()
    game = Game(screen)
    running = True

    while running:
        dt = clock.tick(60) / 1000  # delta‑time w sekundach

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        game.update(dt)
        game.draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

