import pygame


class SpriteAnim:
    """Bardzo prosta animacja: klatki obok siebie w jednym pliku,
    stały FPS, pętla."""

    def __init__(self, sheet_path: str, frames: int, fps: int = 8, scale: int = 2):
        sheet = pygame.image.load(sheet_path).convert_alpha()
        sw, sh = sheet.get_size()
        self.FRAME_W = sw // frames
        self.FRAME_H = sh
        self.frames = [
            pygame.transform.scale(
                sheet.subsurface(x * self.FRAME_W, 0, self.FRAME_W, self.FRAME_H),
                (self.FRAME_W * scale, self.FRAME_H * scale),
            )
            for x in range(frames)
        ]
        self.fps = fps
        self.timer = 0.0
        self.index = 0

    def update(self, dt: float) -> None:
        self.timer += dt
        if self.timer >= 1 / self.fps:
            self.timer = 0.0
            self.index = (self.index + 1) % len(self.frames)

    @property
    def image(self) -> pygame.Surface:
        return self.frames[self.index]
