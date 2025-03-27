import datetime
from globals import *


class DigitFly:
    def __init__(self,
                 hint: str,
                 px: float = LINE_RECT.centerx, py: float = LINE_RECT.centery):
        self.status: int = STATUS.ACTIVE
        self.screen: pygame.Surface = SCREEN
        self.hint: str = hint
        self.px = px
        self.py = py
        self.color_from: Color = COLOR.YELLOW
        self.color_to: Color = COLOR.RED

        self.direction: float = 270
        self.distance: float = 90
        self.move_steps = 10
        self.move_time_frame = timedelta(milliseconds=(1000 / (self.move_steps - 1)))

        self.font_size_from: int = 160
        self.font_size_to: int = 14
        self.font = pygame.font.Font(None, self.font_size_from)

        r1, g1, b1, a1 = self.color_from
        r2, g2, b2, a2 = self.color_to
        dr: float = (r2 - r1) / (self.move_steps - 1)
        dg: float = (g2 - g1) / (self.move_steps - 1)
        db: float = (b2 - b1) / (self.move_steps - 1)
        self.images: list = []
        r: float
        g: float
        b: float
        r, g, b = r1, g1, b1

        font_size: float = self.font_size_from
        font_ds: float = (self.font_size_to - self.font_size_from) / (self.move_steps - 1)

        index = 0
        while index < self.move_steps:
            self.images.append(pygame.font.Font(None, int(font_size)).render(str(self.hint), ANTIALIASING, Color(round(r), round(g), round(b))))
            font_size += font_ds
            r += dr
            g += dg
            b += db
            index += 1
        # print(f"Количество фреймов: {len(self.images)}")
        self.rect: pygame.Rect = self.images[0].get_rect()
        self.draw_index = 0
        self.draw_time_next: datetime = datetime.now() + self.move_time_frame

    def update(self):
        now: datetime = datetime.now()
        if self.draw_time_next <= now:
            self.draw_time_next = now + self.move_time_frame
            self.draw_index += 1
            if self.draw_index == self.move_steps:
                self.draw_index = None
                self.status = STATUS.NONE

    def draw(self):
        if self.draw_index is not None:
            self.rect = self.images[self.draw_index].get_rect()
            self.rect.center = (self.px, self.py)
            self.screen.blit(self.images[self.draw_index], self.rect)
