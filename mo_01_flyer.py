import pygame
from pygame.rect import RectType
from globals import SCREEN_W, SCREEN_H
from military_object import MilitaryObject, MS, Delta

# from military_object import *

image_left = pygame.image.load("img/mo_01/01_l.png")
image_right = pygame.image.load("img/mo_01/01_r.png")


class Fly01(MilitaryObject):
    title: str = "Этажерка"

    STATUS_IMAGES = {
        MS.IDLE: [image_left],
        MS.DEAD: [
            pygame.image.load("img/mo_01/01_dn01.png"),
            pygame.image.load("img/mo_01/01_dn02.png"),
            pygame.image.load("img/mo_01/01_dn03.png"),
            pygame.image.load("img/mo_01/01_dn04.png"),
            pygame.image.load("img/mo_01/01_dn05.png"),
            pygame.image.load("img/mo_01/01_dn06.png")
        ],
        MS.EXPLODE: [
            pygame.image.load("img/mo_01/01_dn06.png")
        ],

        MS.FIRE_A000: [image_right],
        MS.FIRE_A045: [image_right],
        MS.FIRE_A090: [image_right],
        MS.FIRE_A135: [image_left],
        MS.FIRE_A180: [image_left],
        MS.FIRE_A225: [image_left],
        MS.FIRE_A270: [image_left],
        MS.FIRE_A315: [image_right],

        MS.MOVE_A000: [image_right],
        MS.MOVE_A045: [image_right],
        MS.MOVE_A090: [image_right],
        MS.MOVE_A135: [image_left],
        MS.MOVE_A180: [image_left],
        MS.MOVE_A225: [image_left],
        MS.MOVE_A270: [image_left],
        MS.MOVE_A315: [image_right]
    }

    DRAW_SHIFT = {  # dx, dy
        MS.MOVE_A000: Delta(-15, -10),
        MS.MOVE_A045: Delta(-15, -10),
        MS.MOVE_A090: Delta(-15, -10),
        MS.MOVE_A135: Delta(15, -10),
        MS.MOVE_A180: Delta(15, -10),
        MS.MOVE_A225: Delta(15, -10),
        MS.MOVE_A270: Delta(15, -10),
        MS.MOVE_A315: Delta(-15, -10)
    }

    def __init__(self):
        super().__init__(status_start=MS.MOVE_A000,
                         movement_rect=RectType(0, 0, SCREEN_W, SCREEN_H // 2),
                         start_move=True)

    def update_move_to(self, px: float, py: float):
        px, py = super().update_move_to(px=px, py=py)
        if not self.action_move_to:
            self.move_to = self.get_next_point_to()
            self.action_move_to = True
        return px, py
