import pygame


class Minimap:
    CELL    = 14
    GAP     = 3
    PAD     = 16
    OUTLINE = (240, 240, 240)

    COLOR_ACTIVE   = (255, 230,  80)   # żółty
    COLOR_CLEARED  = (150, 150, 150)   # jasny szary
    COLOR_VISITED  = ( 80,  80,  80)   # ciemny szary
    COLOR_UNKNOWN  = ( 40,  40,  40)   # grafit

    def __init__(self, level):
        self.level = level            # referencja do Level

    # ------------------------------------------------------------------
    def draw(self, surf: pygame.Surface) -> None:
        grid = self.level.GRID_SIZE
        sw, _ = surf.get_size()

        start_x = sw - (self.CELL + self.GAP) * grid - self.PAD
        start_y = self.PAD

        cleared = set(self.level.cleared_rooms())
        visited = self.level.visited

        for y in range(grid):
            for x in range(grid):
                pos = (x, y)
                if pos == self.level.current:
                    color = self.COLOR_ACTIVE
                elif pos in cleared:
                    color = self.COLOR_CLEARED
                elif pos in visited:
                    color = self.COLOR_VISITED
                else:
                    color = self.COLOR_UNKNOWN

                rx = start_x + x * (self.CELL + self.GAP)
                ry = start_y + y * (self.CELL + self.GAP)

                pygame.draw.rect(surf, color, (rx, ry, self.CELL, self.CELL))
                pygame.draw.rect(surf, self.OUTLINE, (rx, ry, self.CELL, self.CELL), 2)
