import pygame


class Minimap:
    CELL = 14         # wielkość kwadracika (było 14)
    GAP  = 3          # odstęp między nimi
    PAD  = 16         # od krawędzi ekranu
    OUTLINE = (240, 240, 240)   # ramka

    def __init__(self, level):
        self.level = level          # referencja do Level

    def draw(self, surf: pygame.Surface) -> None:
        grid = self.level.GRID_SIZE
        sw, _ = surf.get_size()

        start_x = sw - (self.CELL + self.GAP) * grid - self.PAD
        start_y = self.PAD

        for y in range(grid):
            for x in range(grid):
                room   = self.level.rooms[y][x]
                active = (x, y) == self.level.current

                # kolor wg stanu
                if active:
                    color = (255, 230, 80)      # żółty – aktualny
                elif room.visited:
                    color = (140, 140, 140)     # jasnoszary – odwiedzony
                else:
                    color = (60, 60, 60)        # ciemny – nieznany

                rx = start_x + x * (self.CELL + self.GAP)
                ry = start_y + y * (self.CELL + self.GAP)

                # wypełnienie
                pygame.draw.rect(surf, color, (rx, ry, self.CELL, self.CELL))
                # obramowanie
                pygame.draw.rect(surf, self.OUTLINE, (rx, ry, self.CELL, self.CELL), 2)

