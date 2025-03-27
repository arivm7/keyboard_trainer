import pygame
from pygame.rect import RectType
from globals import SCREEN_W, SCREEN_H, SCREEN, STATUS, FPS, COLOR


class ImageFly:
    def __init__(self,
                 image: pygame.Surface,
                 px: float = SCREEN_W / 2,
                 py: float = SCREEN_H / 2,
                 px_to: float = SCREEN_W / 2,
                 py_to: float = SCREEN_H / 2,
                 scale_to: float = 0.3,
                 time_to_end: int = 1500,  # миллисекунд до выключения
                 screen: pygame.Surface = SCREEN):
        self.status: int = STATUS.ACTIVE
        self.screen: pygame.Surface = screen
        self.image_original: pygame.Surface = image
        self.image: pygame.Surface = self.image_original.copy()
        self.px: float = px
        self.py: float = py
        self.px_to: float = px_to
        self.py_to: float = py_to
        self.scale_to: float = scale_to

        self.width: float = self.image.get_width()
        self.height: float = self.image.get_height()
        self.rect: RectType = self.image.get_rect()
        self.rect.center = (self.px, self.py)
        self.first_image: bool = True

        self.move_steps: int = round(time_to_end * FPS / 1000)  # количество кадров для отрисовки изображения
        self.dx: float = (self.px_to - self.px) / self.move_steps
        self.dy: float = (self.py_to - self.py) / self.move_steps
        self.scale_per_step: float = (1 - self.scale_to) / self.move_steps
        self.scale_dw: float = self.scale_per_step * self.width
        self.scale_dh: float = self.scale_per_step * self.height

    def update(self):
        if self.first_image:
            self.first_image = False
        else:
            if self.move_steps > 0:
                self.px += self.dx
                self.py += self.dy
                self.width -= self.scale_dw
                self.height -= self.scale_dh
                self.image = pygame.transform.scale(self.image_original, (self.width, self.height))
                self.rect = self.image.get_rect()
                self.rect.center = (self.px, self.py)
                self.move_steps -= 1
            else:
                if self.status == STATUS.ACTIVE:
                    self.status = STATUS.END
                    self.width = self.width * 2
                    self.height = self.height * 2
                if (self.width >0) & (self.height > 0):
                    self.width -= self.scale_dw * 2
                    self.height -= self.scale_dh * 2
                    self.rect = RectType(0, 0, round(self.width), round(self.height))
                    self.rect.center = (self.px, self.py)
                else:
                    self.status = STATUS.NONE

    def draw(self):
        if self.status == STATUS.ACTIVE:
            self.screen.blit(self.image, self.rect)
        elif self.status == STATUS.END:
            margin: int = 2
            pygame.draw.polygon(
                surface=self.screen,
                color=COLOR.YELLOW,
                points=[
                    (self.rect.centerx, self.rect.y),
                    (self.rect.centerx + margin, self.rect.centery - margin),
                    (self.rect.right, self.rect.centery),
                    (self.rect.centerx + margin, self.rect.centery + margin),
                    (self.rect.centerx, self.rect.bottom),
                    (self.rect.centerx - margin, self.rect.centery + margin),
                    (self.rect.left, self.rect.centery),
                    (self.rect.centerx - margin, self.rect.centery - margin)
                ])
        else:
            pass
