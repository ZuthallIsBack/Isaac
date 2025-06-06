"""Zarządzanie siatką pokoi, kolizją ze ścianami oraz rysowaniem aktywnego pokoju."""
import pygame
from pygame import Vector2
from .room import Room


class Level:
    GRID_SIZE = 3

    def __init__(self):
        # ➌ -- przekazujemy GRID_SIZE każdemu Room
        self.rooms: list[list[Room]] = [
            [Room((x, y), self.GRID_SIZE) for x in range(self.GRID_SIZE)]
            for y in range(self.GRID_SIZE)
        ]
        self.current = (1, 1)

    # ───────────────────────────────────────────────────────── ROOM ACCESS ──
    def active_room(self) -> Room:
        return self.rooms[self.current[1]][self.current[0]]

    def change_room(self, dx: int, dy: int) -> None:
        x, y = self.current
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.GRID_SIZE and 0 <= ny < self.GRID_SIZE:
            self.current = (nx, ny)

    # ─────────────────────────────────────────────────────── WORLD OFFSET ───
    # ─────────────────────────────────────────────────────── WORLD OFFSET ───
    def world_offset(self) -> Vector2:
        """Przesunięcie kamery tak, aby aktywny pokój był WYŚRODKOWANY
        (nie przyklejony w lewy-górny róg)."""
        room = self.active_room()

        # pobieramy rozmiar bieżącego okna
        screen_w, screen_h = pygame.display.get_surface().get_size()

        # ile wolnego miejsca zostaje po bokach
        pad_x = (screen_w - Room.SIZE[0]) // 2
        pad_y = (screen_h - Room.SIZE[1]) // 2

        # przesuwamy scenę: –room.rect + padding
        return Vector2(-room.rect.x + pad_x, -room.rect.y + pad_y)

    # ─────────────────────────────────────────────────────────── UPDATE ─────
    def update(self, player) -> None:
        room = self.active_room()

        # ===== sprawdzenie wyjścia przez drzwi =====
        margin = 16
        dx = dy = 0
        if player.rect.top < room.rect.top - margin:
            dy = -1
        elif player.rect.bottom > room.rect.bottom + margin:
            dy = 1
        elif player.rect.left < room.rect.left - margin:
            dx = -1
        elif player.rect.right > room.rect.right + margin:
            dx = 1

        if dx or dy:
            self.change_room(dx, dy)
            room = self.active_room()
            # teleport gracza tuż za próg (jak wcześniej)
            if dx == -1:
                player.pos.x = room.rect.right - margin - player.rect.width
            elif dx == 1:
                player.pos.x = room.rect.left + margin
            if dy == -1:
                player.pos.y = room.rect.bottom - margin - player.rect.height
            elif dy == 1:
                player.pos.y = room.rect.top + margin
            player.rect.topleft = player.pos

        # ===== kolizja z ścianą =====
        walk_area = room.inner_rect()
        if not walk_area.contains(player.rect):
            in_door = any(player.rect.colliderect(dr) for dr in room.door_rects())
            if not in_door:
                if player.rect.left < walk_area.left:
                    player.pos.x = walk_area.left
                if player.rect.right > walk_area.right:
                    player.pos.x = walk_area.right - player.rect.width
                if player.rect.top < walk_area.top:
                    player.pos.y = walk_area.top
                if player.rect.bottom > walk_area.bottom:
                    player.pos.y = walk_area.bottom - player.rect.height
                player.rect.topleft = player.pos

    # ───────────────────────────────────────────────────────────── DRAW ─────
    def draw(self, surface: pygame.Surface) -> None:
        # renderujemy tylko aktywny pokój; sąsiednie zostaną ukryte
        offset = self.world_offset()
        self.active_room().draw(surface, offset)