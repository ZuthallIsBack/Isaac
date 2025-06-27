"""Zarządzanie siatką pokoi, kolizją ze ścianami oraz rysowaniem aktywnego pokoju."""
import pygame
from pygame import Vector2
from .room import Room
from entities.pickup import Heart
from entities.chest import Chest
import random


class Level:
    GRID_SIZE = 3

    def __init__(self):
        # ➌ -- przekazujemy GRID_SIZE każdemu Room
        self.rooms = [
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
        if not room.doors_open:
            walk_through_doors = False
        else:
            walk_through_doors = True
        dx = dy = 0
        if walk_through_doors and player.rect.top < room.rect.top - margin:
            dy = -1
        elif walk_through_doors and player.rect.bottom > room.rect.bottom + margin:
            dy = 1
        elif walk_through_doors and player.rect.left < room.rect.left - margin:
            dx = -1
        elif walk_through_doors and player.rect.right > room.rect.right + margin:
            dx = 1

        if dx or dy:
            self.change_room(dx, dy)
            new_room = self.active_room()
            new_room.enter()  # SPawn przeciwników + zamknięcie drzwi
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

        alive = [e for e in room.enemies if not getattr(e, "dying", False)]
        if not room.doors_open and not alive:  # ← UŻYWAMY 'alive'
            room.doors_open = True
            room.cleared = True

            # 50 % szansy na serce
            if random.random() < 0.5:
                rx = random.randint(room.rect.left + 50, room.rect.right - 50)
                ry = random.randint(room.rect.top + 50, room.rect.bottom - 50)
                room.pickups.append(Heart((rx, ry)))


            if random.random() < 0.3:
                cx = random.randint(room.rect.left + 60, room.rect.right - 60)
                cy = random.randint(room.rect.top + 60, room.rect.bottom - 60)
                room.pickups.append(Chest((cx, cy)))

    # ───────────────────────────────────────────────────────────── DRAW ─────
    def draw(self, surface: pygame.Surface) -> None:
        # renderujemy tylko aktywny pokój; sąsiednie zostaną ukryte
        offset = self.world_offset()
        self.active_room().draw(surface, offset)