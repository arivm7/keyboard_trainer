from mo_bullet import Bullet
from military_object import *

image_left1 = pygame.image.load("img/mo_02/vetka_200_lf_01.png")
image_right1 = pygame.image.load("img/mo_02/vetka_200_rg_01.png")


class Fly02_Vetka(MilitaryObject):
    title: str = "Ветка"
    speed_move_interval: Interval = Interval(10, 20)  # Интервал автоматического назначения скорости движения
    parking_place: bool = True  # На объект можно припарковаться

    STATUS_IMAGES = {
        MS.IDLE: [image_left1],
        MS.DEAD: [None],
        MS.EXPLODE: [None],

        MS.FIRE_A000: [image_right1],
        MS.FIRE_A045: [image_right1],
        MS.FIRE_A090: [image_right1],
        MS.FIRE_A135: [image_left1],
        MS.FIRE_A180: [image_left1],
        MS.FIRE_A225: [image_left1],
        MS.FIRE_A270: [image_left1],
        MS.FIRE_A315: [image_right1],

        MS.MOVE_A000: [image_right1],
        MS.MOVE_A045: [image_right1],
        MS.MOVE_A090: [image_right1],
        MS.MOVE_A135: [image_left1],
        MS.MOVE_A180: [image_left1],
        MS.MOVE_A225: [image_left1],
        MS.MOVE_A270: [image_left1],
        MS.MOVE_A315: [image_right1]
    }

    DRAW_SHIFT = {  # dx, dy
        DIRECTION.A000: Delta(0, 0),
        DIRECTION.A045: Delta(0, 0),
        DIRECTION.A090: Delta(0, 0),
        DIRECTION.A135: Delta(0, 0),
        DIRECTION.A180: Delta(0, 0),
        DIRECTION.A225: Delta(0, 0),
        DIRECTION.A270: Delta(0, 0),
        DIRECTION.A315: Delta(0, 0)
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

    def fire(self, target: object):
        bullet = Bullet(start_from=Point(self.px, self.py), attack_to=AttackTo(None, None, None, target))
        ACTORS.append(bullet)

