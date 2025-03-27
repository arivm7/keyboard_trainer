import pygame.font
from pygame.rect import RectType
from pygame import Color
from globals import COLOR, FONT_DEFAULT, SCREEN, ANTIALIASING, get_font_default


class TSimpleScroller:
    def __init__(self,
                 title: str,
                 rect: RectType,
                 value_start: float,
                 value_end: float,
                 color_title: Color = COLOR.TEXT_DEFAULT,
                 color_frame: Color = COLOR.BLACK20,
                 color_bk: Color = COLOR.BLACK90,
                 color_scroller_process: Color = COLOR.YELLOW,
                 color_scroller_end: Color = COLOR.GREEN,
                 title_font: pygame.font.Font = None,
                 screen: pygame.surface.Surface = SCREEN
                 ):
        self.screen: pygame.surface.Surface = screen
        self.title: str = title
        if title_font is None:
            self.title_font: pygame.font.Font = get_font_default(font_size=20)
        else:
            self.title_font: pygame.font.Font = title_font
        self.value_start: float = value_start
        self.value_end: float = value_end
        self.value: float = self.value_start
        self.rect: RectType = rect
        self.rect_scroller: RectType = RectType(self.rect.x + 2, self.rect.y + 2, self.rect.w - 4, self.rect.h - 4)
        self.color_title: Color = color_title
        self.color_frame: Color = color_frame
        self.color_bk: Color = color_bk
        self.color_scroller_process: Color = color_scroller_process
        self.color_scroller_end: Color = color_scroller_end
        self.scroller_point: float = (self.value_end - self.value_start + 1) / self.rect_scroller.width * 4
        self.point_step: float = 0.0
        self.k = self.rect_scroller.width / (self.value_end - self.value_start)
        self.title_img: pygame.surface.Surface = self.title_font.render(self.title, ANTIALIASING, self.color_title)
        self.title_rect: RectType = self.title_img.get_rect()
        self.title_rect.x = self.rect_scroller.x
        self.title_rect.centery = self.rect_scroller.centery

    def draw(self, flip: bool = False):
        self.point_step += 1.0
        if self.point_step > self.scroller_point:
            self.point_step = 0.0
            pygame.draw.rect(surface=self.screen, rect=self.rect, width=0, color=self.color_bk)
            pygame.draw.rect(surface=self.screen, rect=self.rect, width=1, color=self.color_frame)
            rect_scroller: RectType = RectType(self.rect_scroller.x, self.rect_scroller.y, self.k * (self.value - self.value_start), self.rect_scroller.h)
            percent: float = (self.value_end - self.value_start) / 100
            if (self.value_end - self.value) >= percent:
                color = self.color_scroller_process
            else:
                color = self.color_scroller_end
            pygame.draw.rect(surface=self.screen, rect=rect_scroller, width=0, color=color)
            self.screen.blit(self.title_img, self.title_rect)
            if flip:
                pygame.display.flip()



