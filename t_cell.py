import pygame.font
from globals import *


class TCell:
    def __init__(self,
                 text_str: str,
                 padding: int = 5,  # отступ от края ячейки до текста
                 h_align: int = ALIGN.LEFT,  # Горизонтальное выравнивание
                 v_align: int = ALIGN.CENTER,  # вертикальное выравнивание
                 text_color: tuple = COLOR.TEXT_DEFAULT,
                 bk_color: tuple | None = COLOR.BK_DEFAULT,
                 font: pygame.font.Font = FONT_DEFAULT,
                 frame_width: int = 1,
                 frame_color: tuple | None = COLOR.TEXT_DEFAULT):
        self.screen: pygame.Surface = SCREEN
        self.text_str: str = text_str
        self.padding: int = padding
        self.h_align: int = h_align
        self.v_align: int = v_align
        self.text_color: tuple = text_color
        self.bk_color: tuple = bk_color
        self.font: pygame.font.Font = font
        self.frame_width: int = frame_width
        self.frame_color: tuple = frame_color
        self.text_img: pygame.Surface = self.font.render(self.text_str, ANTIALIASING, self.text_color)
        self.text_rect: pygame.Rect = self.text_img.get_rect()

    def width(self) -> int:
        return self.text_rect.width + self.padding * 2

    def height(self) -> int:
        return self.text_rect.height + self.padding * 2

    def rect(self, px: int = 0, py: int = 0) -> RectType:
        return RectType(px, py, self.width(), self.height())

    def draw(self, rect: pygame.Rect):

        # подложка ячейки
        if self.bk_color is not None:
            pygame.draw.rect(self.screen, self.bk_color, rect, width=0)

        # рамка ячейки
        if self.frame_width > 0:
            pygame.draw.rect(self.screen, self.frame_color, rect, width=self.frame_width)

        # рект для вывода текста
        t_rect = RectType(rect.x + self.padding, rect.y + self.padding, rect.w - self.padding * 2, rect.h - self.padding * 2)
        # pygame.draw.rect(self.screen, COLOR.BLACK20, t_rect, self.frame_width)
        # if t_rect.width > self.text_rect.width:
        match self.v_align:
            case ALIGN.TOP:
                self.text_rect.top = t_rect.top
            case ALIGN.CENTER:
                self.text_rect.centery = t_rect.centery
            case ALIGN.BOTTOM:
                self.text_rect.bottom = t_rect.bottom
            case _:
                raise Exception('TCell: draw: Недопустимый v_align')
        # else:
        #     self.text_rect.centerx = t_rect.centerx

        # if t_rect.height > self.text_rect.height:
        match self.h_align:
            case ALIGN.LEFT:
                self.text_rect.left = t_rect.left
            case ALIGN.CENTER:
                self.text_rect.centerx = t_rect.centerx
            case ALIGN.RIGHT:
                self.text_rect.right = t_rect.right
            case _:
                raise Exception('TCell: draw: Недопустимый h_align')
        # else:
        #     self.text_rect.centery = t_rect.centery

        self.screen.blit(self.text_img, self.text_rect)



