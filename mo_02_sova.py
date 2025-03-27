import pygame

from military_object import *

image_left1 = pygame.image.load("img/mo_02/sova_200_lf_01.png")
image_left2 = pygame.image.load("img/mo_02/sova_200_lf_02.png")
image_right1 = pygame.image.load("img/mo_02/sova_200_rg_01.png")
image_right2 = pygame.image.load("img/mo_02/sova_200_rg_02.png")


class Fly02_Sova(MilitaryObject):
    title: str = "Сова"
    parkable: bool = True  # Объект умеет парковаться

    STATUS_IMAGES = {
        MS.IDLE: [image_left1, image_left1, image_left1, image_left2, image_left2],
        MS.DEAD: [None],
        MS.EXPLODE: [None],

        MS.FIRE_A000: [image_right1, image_right1, image_right1, image_right1, image_right1, image_right2, image_right2],
        MS.FIRE_A045: [image_right1, image_right1, image_right1, image_right1, image_right1, image_right2, image_right2],
        MS.FIRE_A090: [image_right1, image_right1, image_right1, image_right1, image_right1, image_right2, image_right2],
        MS.FIRE_A135: [image_left1, image_left1, image_left1, image_left1, image_left1, image_left2, image_left2],
        MS.FIRE_A180: [image_left1, image_left1, image_left1, image_left1, image_left1, image_left2, image_left2],
        MS.FIRE_A225: [image_left1, image_left1, image_left1, image_left1, image_left1, image_left2, image_left2],
        MS.FIRE_A270: [image_left1, image_left1, image_left1, image_left1, image_left1, image_left2, image_left2],
        MS.FIRE_A315: [image_right1, image_right1, image_right1, image_right1, image_right1, image_right2, image_right2],

        MS.MOVE_A000: [image_right1, image_right1, image_right1, image_right1, image_right1, image_right1, image_right2],
        MS.MOVE_A045: [image_right1, image_right1, image_right1, image_right1, image_right1, image_right1, image_right2],
        MS.MOVE_A090: [image_right1, image_right1, image_right1, image_right1, image_right1, image_right1, image_right2],
        MS.MOVE_A135: [image_left1, image_left1, image_left1, image_left1, image_left1, image_left2, image_left2],
        MS.MOVE_A180: [image_left1, image_left1, image_left1, image_left1, image_left1, image_left2, image_left2],
        MS.MOVE_A225: [image_left1, image_left1, image_left1, image_left1, image_left1, image_left2, image_left2],
        MS.MOVE_A270: [image_left1, image_left1, image_left1, image_left1, image_left1, image_left2, image_left2],
        MS.MOVE_A315: [image_right1, image_right1, image_right1, image_right1, image_right1, image_right1, image_right2]
    }

    DRAW_SHIFT = {  # dx, dy
        MS.MOVE_A000: Delta(35, 0),
        MS.MOVE_A045: Delta(35, 0),
        MS.MOVE_A090: Delta(35, 0),
        MS.MOVE_A135: Delta(-35, 0),
        MS.MOVE_A180: Delta(-35, 0),
        MS.MOVE_A225: Delta(-35, 0),
        MS.MOVE_A270: Delta(-35, 0),
        MS.MOVE_A315: Delta(35, 0)
    }

    def __init__(self):
        super().__init__(status_start=MS.MOVE_A000,
                         movement_rect=RectType(0, 0, SCREEN_W, SCREEN_H // 2),
                         start_move=True)

    def update_move_to(self, px: float, py: float):
        px, py = super().update_move_to(px=px, py=py)
        if (self.parked is None) and (not self.action_move_to):
            self.move_to = self.get_next_point_to()
            self.action_move_to = True
        return px, py
