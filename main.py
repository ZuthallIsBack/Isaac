"""Główne uruchomienie gry – nic nie zmieniamy."""
import pygame
from core.game import Game
from audio import play_music, toggle_music

def main() -> None:
    pygame.init()
    pygame.mixer.init()
    play_music()

    WIDTH, HEIGHT = 960, 540
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Isaac Clone")

    clock = pygame.time.Clock()
    game = Game(screen)

    running = True
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                toggle_music()

        game.update(dt)
        game.draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()