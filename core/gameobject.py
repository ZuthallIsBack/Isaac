"""Bazowe klasy dla wszystkich obiektów w grze."""
import pygame


class GameObject:
    """Nieruchomy obiekt z pozycją i prostokątem kolizji."""

    def __init__(self, pos: pygame.Vector2 | tuple[int, int], size: tuple[int, int]):
        self.pos = pygame.Vector2(pos)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, *size)

    def draw(self, surface: pygame.Surface) -> None:  # nadpisywane
        raise NotImplementedError


class MovingObject(GameObject):
    """Obiekt, który może się poruszać (posiada prędkość)."""

    def __init__(self, pos: pygame.Vector2 | tuple[int, int], size: tuple[int, int]):
        super().__init__(pos, size)