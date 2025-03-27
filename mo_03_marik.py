from military_object import *
from mo_bullet import Bullet

images_RC_move = get_images_list_from_folder(folder="img/mo_03_marik/RC_move")
images_RC_fire = get_images_list_from_folder(folder="img/mo_03_marik/RC_fire")

images_RD_move = get_images_list_from_folder(folder="img/mo_03_marik/RD_move")
images_RD_fire = get_images_list_from_folder(folder="img/mo_03_marik/RD_fire")

images_DC_move = images_RD_move
images_DC_fire = images_RD_fire

images_LD_move = get_images_list_from_folder(folder="img/mo_03_marik/LD_move")
images_LD_fire = get_images_list_from_folder(folder="img/mo_03_marik/LD_fire")

images_LC_move = get_images_list_from_folder(folder="img/mo_03_marik/LC_move")
images_LC_fire = get_images_list_from_folder(folder="img/mo_03_marik/LC_fire")

images_LU_move = images_LC_move
images_LU_fire = images_LC_fire

images_UC_move = get_images_list_from_folder(folder="img/mo_03_marik/UC_move")
images_UC_fire = get_images_list_from_folder(folder="img/mo_03_marik/UC_fire")

images_RU_move = images_RC_move
images_RU_fire = images_RC_fire



class Mo03_Marik(MilitaryObject):
    title: str = "Марик"
    speed_move_interval: Interval = Interval(30, 35)  # Интервал автоматического назначения скорости движения
    parking_place: bool = False  # На объект можно припарковаться

    STATUS_IMAGES = {
        MS.IDLE: images_LC_move,
        MS.DEAD: [None],
        MS.EXPLODE: [None],

        MS.MOVE_A000: images_RC_move,
        MS.MOVE_A045: images_RD_move,
        MS.MOVE_A090: images_DC_move,
        MS.MOVE_A135: images_LD_move,
        MS.MOVE_A180: images_LC_move,
        MS.MOVE_A225: images_LU_move,
        MS.MOVE_A270: images_UC_move,
        MS.MOVE_A315: images_RU_move,

        MS.FIRE_A000: images_RC_fire,
        MS.FIRE_A045: images_RD_fire,
        MS.FIRE_A090: images_DC_fire,
        MS.FIRE_A135: images_LD_fire,
        MS.FIRE_A180: images_LC_fire,
        MS.FIRE_A225: images_LU_fire,
        MS.FIRE_A270: images_UC_fire,
        MS.FIRE_A315: images_RU_fire,

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
        if self.status in [MS.FIRE_RC, MS.FIRE_RD, MS.FIRE_DC, MS.FIRE_LD, MS.FIRE_LC, MS.FIRE_LU, MS.FIRE_UC, MS.FIRE_RU]:
            return px, py
        px, py = super().update_move_to(px=px, py=py)
        if not self.action_move_to:
            self.move_to = self.get_next_point_to()
            self.action_move_to = True
        return px, py

    def fire(self, target: MilitaryObject):
        w = self.rect.width / 2
        h = self.rect.height / 2
        match self.discrete_direction:
            case DIRECTION.A000:
                start = Point(self.px + w, self.py + 0)
            case DIRECTION.A045:
                start = Point(self.px + w, self.py - h)
            case DIRECTION.A090:
                start = Point(self.px + 0, self.py - h)
            case DIRECTION.A135:
                start = Point(self.px - w, self.py - h)
            case DIRECTION.A180:
                start = Point(self.px - w, self.py + 0)
            case DIRECTION.A225:
                start = Point(self.px - w, self.py + h)
            case DIRECTION.A270:
                start = Point(self.px + 0, self.py + h)
            case DIRECTION.A315:
                start = Point(self.px + w, self.py + h)
            case _:
                exit("marik.fire: Этого не должно быть(1)")

        a = get_angle(self.px, self.py, target.px, target.py)
        # !!! Сюда вписать пересчет по углу
        bullet = Bullet(start_from=start,
                        attack_to=AttackTo(None, None, None, target),
                        speed_px_sec=110)
        ACTORS.append(bullet)
