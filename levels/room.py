"""Pojedynczy pokój – teraz ze ścianką kolizji i opisem drzwi."""
import pygame
import random
from entities.enemy import Bat, Slime

class Room:
    SIZE = (800, 450)
    WALL_THICK = 8
    BG_COLOR = (40, 40, 40)
    DOOR_COLOR = (120, 120, 120)
    DOOR_W, DOOR_H = 64, 32

    def __init__(self, grid_pos: tuple[int, int], grid_size: int):
        self.grid_x, self.grid_y = grid_pos
        self.grid_size = grid_size
        self.rect = pygame.Rect(
            self.grid_x * self.SIZE[0],
            self.grid_y * self.SIZE[1],
            *self.SIZE,
        )
        self.enemies: list = []
        self.pickups: list = []
        self.visited = False
        self.doors_open = True

    # ─────────────────────────────────────────────────────────── HELPERS ────
    def inner_rect(self) -> pygame.Rect:
        """Obszar, po którym można chodzić (bez ścian)."""
        return self.rect.inflate(-self.WALL_THICK * 2, -self.WALL_THICK * 2)

    # ───────────────────────── enter room ─────────────────────────
    def enter(self):
        """Wywołaj przy wejściu gracza – spawn przeciwników i zamknięcie drzwi."""
        if not self.visited:
            from entities.enemy import Bat      # lokalny import (unikamy pętli)
            self.enemies = []
            self.pickups = []
            for _ in range(3):
                rx = random.randint(self.rect.left + 60, self.rect.right - 60)
                ry = random.randint(self.rect.top + 60, self.rect.bottom - 60)

                # 50 % szans: Slime • 50 %: Bat
                if random.random() < 0.3:
                    self.enemies.append(Slime((rx, ry)))
                else:
                    self.enemies.append(Bat((rx, ry)))
            self.doors_open = False
            self.visited = True


    # ➋ -- drzwi tylko jeśli jest pokój obok
    def door_rects(self) -> list[pygame.Rect]:
        doors: list[pygame.Rect] = []
        cx, cy = self.rect.center

        # góra
        if self.grid_y > 0:
            doors.append(
                pygame.Rect(cx - self.DOOR_W // 2,
                            self.rect.top - 1,
                            self.DOOR_W, self.WALL_THICK)
            )
        # dół
        if self.grid_y < self.grid_size - 1:
            doors.append(
                pygame.Rect(cx - self.DOOR_W // 2,
                            self.rect.bottom - self.WALL_THICK,
                            self.DOOR_W, self.WALL_THICK)
            )
        # lewo
        if self.grid_x > 0:
            doors.append(
                pygame.Rect(self.rect.left - 1,
                            cy - self.DOOR_H // 2,
                            self.WALL_THICK, self.DOOR_H)
            )
        # prawo
        if self.grid_x < self.grid_size - 1:
            doors.append(
                pygame.Rect(self.rect.right - self.WALL_THICK,
                            cy - self.DOOR_H // 2,
                            self.WALL_THICK, self.DOOR_H)
            )
        return doors

    # ───────────────────────────────────────────────────────────── DRAW ─────
    def draw(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        room_rect = self.rect.move(offset)
        pygame.draw.rect(surface, self.BG_COLOR, room_rect)
        pygame.draw.rect(surface, (20, 20, 20), room_rect, self.WALL_THICK)
        door_color = self.DOOR_COLOR if self.doors_open else (140, 0, 0)
        for dr in self.door_rects():
            pygame.draw.rect(surface, door_color, dr.move(offset))
