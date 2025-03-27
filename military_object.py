from random import choices, randint

from control import *
import datetime
from collections import namedtuple
import pygame.sprite
from pygame import Color
from pygame.event import EventType
from pygame.font import FontType
from pygame.rect import RectType

# Point = namedtuple('Point', ['x', 'y'])  # Описан в pygame.draw_py
Delta = namedtuple('Delta', ['dx', 'dy'])
Interval = namedtuple('Interval', ['v1', 'v2'])
AttackTo = namedtuple('AttackTo', ['x', 'y', 'direction', 'object'])

half_sector: float = 45 / 2  # Половина сектора. Для вычисления границ секторов направлений


class MS:  # Military Status
    IDLE: int =     10001
    JUMP: int =     10002
    FLY: int =      10003
    FIRE_RC: int =  10004
    FIRE_RD: int =  10005
    FIRE_DC: int =  10006
    FIRE_LD: int =  10007
    FIRE_LC: int =  10008
    FIRE_LU: int =  10009
    FIRE_UC: int =  10010
    FIRE_RU: int =  10011

    FIRE_A000: int = FIRE_RC
    FIRE_A045: int = FIRE_RD
    FIRE_A090: int = FIRE_DC
    FIRE_A135: int = FIRE_LD
    FIRE_A180: int = FIRE_LC
    FIRE_A225: int = FIRE_LU
    FIRE_A270: int = FIRE_UC
    FIRE_A315: int = FIRE_RU

    MOVE_RC: int =  10012
    MOVE_RD: int =  10013
    MOVE_DC: int =  10014
    MOVE_LD: int =  10015
    MOVE_LC: int =  10016
    MOVE_LU: int =  10017
    MOVE_UC: int =  10018
    MOVE_RU: int =  10019

    MOVE_A000: int = MOVE_RC
    MOVE_A045: int = MOVE_RD
    MOVE_A090: int = MOVE_DC
    MOVE_A135: int = MOVE_LD
    MOVE_A180: int = MOVE_LC
    MOVE_A225: int = MOVE_LU
    MOVE_A270: int = MOVE_UC
    MOVE_A315: int = MOVE_RU

    EXPLODE: int =  10020
    DEAD: int =     10021
    PREV: int =     10022  # флаг перехода к предыдущему статусу
    NONE: int =     10023


class DIRECTION:
    RC = A000 = 0
    RD = A045 = 45
    DC = A090 = 90
    LD = A135 = 135
    LC = A180 = 180
    LU = A225 = 225
    UC = A270 = 270
    RU = A315 = 315

    RC_FROM: float = 360 - half_sector
    RC_TO: float = 0 + half_sector
    RD_FROM: float = RD - half_sector
    RD_TO: float = RD + half_sector
    DC_FROM: float = DC - half_sector
    DC_TO: float = DC + half_sector
    LD_FROM: float = LD - half_sector
    LD_TO: float = LD + half_sector
    LC_FROM: float = LC - half_sector
    LC_TO: float = LC + half_sector
    LU_FROM: float = LU - half_sector
    LU_TO: float = LU + half_sector
    UC_FROM: float = UC - half_sector
    UC_TO: float = UC + half_sector
    RU_FROM: float = RU - half_sector
    RU_TO: float = RU + half_sector


# BODY MODE STATUS
BODY_SOLID: int = auto_id()  # Твёрдое тело
BODY_SOFT: int = auto_id()  # Мягкое тело, через него проходят другие объекты на экране


def get_discrete_direction(angle: float | None) -> int | None:
    if (angle is not None) and (angle < 0):
        angle = 360 + angle
    if angle is None:
        return None
    elif (DIRECTION.RC_FROM <= angle <= 360) or (0 <= angle <= DIRECTION.RC_TO):
        return DIRECTION.RC
    elif DIRECTION.RD_FROM <= angle <= DIRECTION.RD_TO:
        return DIRECTION.RD
    elif DIRECTION.DC_FROM <= angle <= DIRECTION.DC_TO:
        return DIRECTION.DC
    elif DIRECTION.LD_FROM <= angle <= DIRECTION.LD_TO:
        return DIRECTION.LD
    elif DIRECTION.LC_FROM <= angle <= DIRECTION.LC_TO:
        return DIRECTION.LC
    elif DIRECTION.LU_FROM <= angle <= DIRECTION.LU_TO:
        return DIRECTION.LU
    elif DIRECTION.UC_FROM <= angle <= DIRECTION.UC_TO:
        return DIRECTION.UC
    elif DIRECTION.RU_FROM <= angle <= DIRECTION.RU_TO:
        return DIRECTION.RU
    else:
        raise Exception(f"get_discrete_direction: Угол {angle} не найден в таблице направлений")
        # sys.exit(1)


class CROSS_DRAW:  # Крестик положения, эллипс размера и линия направления движения
    UP = POST = auto_id()  # Рисовать сверху
    DOWN = PRE = auto_id()  # Рисовать позади объекта
    OFF = auto_id()  # Не рисовать

class DAMAGE:
    ALL = auto_id()
    ALIENS = auto_id()
    NO = auto_id()

ACTORS: list[pygame.sprite.Sprite] = []


class MilitaryObject(pygame.sprite.Sprite):
    id: int
    title: str = "MilitaryObject"
    title_font_default: pygame.font.Font = get_font_default(font_size=12)
    title_color = Color(43, 90, 63, 255)
    title_font: FontType = title_font_default
    title_to_draw: bool = True  # выводить на экран название

    hp_interval: Interval = Interval(100, 500)  # Интервал автоматического назначения hp
    hp_font_default: pygame.font.Font = get_font_default(font_size=12)
    hp_to_draw: bool = True  # выводить на экран hp

    damage_who: int = DAMAGE.ALIENS  # Признак-указатель того, кому наносится урон
    damage_value: float | None = None  # Величина повреждения другому объекту
    damage_radius: float | None = None  # Радиус поражения. Максимум в центре и 0 в конце радиуса поражения

    cross_draw = CROSS_DRAW.PRE  # Крестик положения, эллипс размера и линия направления движения
    target_next_wait_ms: int = 60000  # milliseconds время для смены точки цели, чтобы избавиться от "спутников".
    target_next_time_now: datetime = datetime.datetime.now()  # Время, когда нужно назначить другую цель движения
    hairs_color = Color(25, 45, 35, 255)

    speed_move_interval: Interval = Interval(25, 60)  # Интервал автоматического назначения скорости движения
    speed_rotate_interval: Interval = Interval(25, 60)  # Интервал автоматического назначения скорости вращения
    direction_interval: Interval = Interval(0, 359)  # Интервал автоматического назначения направления движения

    parking_place: bool = False  # На объект можно припарковаться
    parkable: bool = False  # Объект умеет парковаться

    image_next_wait_ms: int = 1000 / 15  # milliseconds интервал смены картинок спрайтов (15 FPS)
    image_next_time_now: datetime = datetime.datetime.now()  # Время, когда можно менять картинку на следующую.

    rotate_and_move = True  # 0 - Сперва поворачивать, а потом двигаться
    rotate_inertial_move = True  # При смене направления движения двигаться далее по инерции одновременно с поворотом. Только при rotate_and_move == True
    rotate_in_place_angle = 90  # при отключенном rotate_and_move указывает угол до цели, при котором начинать движение

    # режимы:
    # СТОЯНИЕ / ОЖИДАНИЕ
    # АТАКА
    # ДВИЖЕНИЕ
    # ВЗРЫВ

    STATUS_IMAGES = {
        # MS.IDLE: list,  # pygame.Surface
        # MS.DEAD: list,  # pygame.Surface
        # MS.FLY: list,  # pygame.Surface
        # MS.EXPLODE: list,  # pygame.Surface
        #
        # MS.FIRE_RC: list,  # pygame.Surface
        # MS.FIRE_RD: list,  # pygame.Surface
        # MS.FIRE_DC: list,  # pygame.Surface
        # MS.FIRE_LD: list,  # pygame.Surface
        # MS.FIRE_LC: list,  # pygame.Surface
        # MS.FIRE_LU: list,  # pygame.Surface
        # MS.FIRE_UC: list,  # pygame.Surface
        # MS.FIRE_RU: list,  # pygame.Surface
        #
        # MS.MOVE_RC: list,  # pygame.Surface
        # MS.MOVE_RD: list,  # pygame.Surface
        # MS.MOVE_DC: list,  # pygame.Surface
        # MS.MOVE_LD: list,  # pygame.Surface
        # MS.MOVE_LC: list,  # pygame.Surface
        # MS.MOVE_LU: list,  # pygame.Surface
        # MS.MOVE_UC: list,  # pygame.Surface
        # MS.MOVE_RU: list   # pygame.Surface
    }

    # Смещение позиции отрисовки спрайта от позиционной точки px py в зависимости от своего направления
    height_over_ground = 0  # расстояние точки вращения px py от поверхности земли
    DRAW_SHIFT = {  # dx, dy
        MS.MOVE_A000: Delta(0, 0),
        MS.MOVE_A045: Delta(0, 0),
        MS.MOVE_A090: Delta(0, 0),
        MS.MOVE_A135: Delta(0, 0),
        MS.MOVE_A180: Delta(0, 0),
        MS.MOVE_A225: Delta(0, 0),
        MS.MOVE_A270: Delta(0, 0),
        MS.MOVE_A315: Delta(0, 0)
    }

    # MS-Статусы, которые выполняются один раз,
    # за тем статус меняется на указанный
    displayed_once = {
        MS.JUMP: MS.PREV,
        MS.FIRE_RC: MS.PREV,
        MS.FIRE_LC: MS.PREV,
        MS.FIRE_UC: MS.PREV,
        MS.FIRE_DC: MS.PREV,
        MS.FIRE_RU: MS.PREV,
        MS.FIRE_RD: MS.PREV,
        MS.FIRE_LU: MS.PREV,
        MS.FIRE_LD: MS.PREV,
        MS.EXPLODE: MS.DEAD,
        MS.DEAD: MS.NONE
    }

    # MS-Статусы, которые не изменяют направления.
    # Должны быть заканчиваться сами, т.е. находиться в словаре displayed_once
    unrotable_statuses = [
        MS.JUMP,
        MS.EXPLODE,
        MS.DEAD
    ]

    def __init__(self,
                 px: float = None,
                 py: float = None,
                 attack_to: AttackTo | None = None,
                 speed_px_sec: float = None,  # пикселей в секунду
                 speed_grad_sec: float = None,  # градусов в секунду
                 hp_value: int = None,  # величина здоровья/жизни
                 movement_rect: RectType = None,  # прямоугольник в котором двигается объект
                 status_start: int = None,  # Стартовый статус
                 start_move: bool = False,
                 start_direction: float = None,
                 start_move_to: Point | None = None,  # координаты точки к которой движется
                 start_rotate: bool = False,  # поворачивать в указанное направление
                 start_rotate_to: float | None = None,  # направление в которое поворачивается если self.action_rotate_to = True
                 screen: pygame.Surface = SCREEN
                 ):
        super().__init__()
        self.id = auto_id()
        self.screen: pygame.Surface = screen

        self.yours: list = []  # свои
        self.yours_distance: int = SCREEN_H // 4  # Пикселей. Расстояние на котором регистрируются объекты

        self.aliens: list = []  # враги
        self.aliens_distance: int = SCREEN_H // 4  # Пикселей. Расстояние на котором регистрируются объекты
        # self.weapon: pygame.sprite.Sprite = None
        self.damage_to: float = 0  # повреждение того, с кем столкнулись
        self.damage_my: float = 0  # повреждение себя при столкновении с кем то
        self.recharge_wait_ms = 500  # milliseconds # время перезарядки при стрельбе
        self.recharge_time_now: datetime = datetime.datetime.now() + timedelta(milliseconds=self.recharge_wait_ms)  # время готовности к выстрелу

        self.ignores: list = []  # список объектов, которые игнорируются при движении
        self.ignores_distance: int = SCREEN_H // 4  # Пикселей. Расстояние на котором регистрируются объекты

        self.parkings: list = []  # Если есть объекты, то перемещаться в координаты найденного
        self.parkings_distance: int = SCREEN_W // 4  # Пикселей. Расстояние на котором регистрируются объекты
        self._parked: pygame.sprite.Sprite | None = None  # MilitaryObject -- Объект, к которому уже припаркован. Далее рисуется в координатах этого объекта

        self.action_move_to: bool = start_move  # действие "движение" активно
        self._move_to: Point | None = None  # координаты точки к которой движется если self.action_move_to = True
        self.move_to: Point = start_move_to   # двигаться к точке
        self._direction: float | None = None  # Реальное направление движения/стояния/ожидания в градусах
        self.discrete_direction: int | None = None  # Дискретное направление движения/стояния/ожидания в градусах

        self.action_rotate_to: bool = start_rotate
        self._rotate_to: float | None = None  # направление в которое поворачивается если self.action_rotate_to = True
        self._status: int = MS.IDLE  # статус для выбора последовательности картинок
        self.status_previous: int = self._status  # предыдущий статус объекта

        # поле разрешенного движения объекта
        if movement_rect is not None:
            self.movement_rect: RectType = movement_rect
        else:
            self.movement_rect: RectType = RectType(0, 0, SCREEN_W, SCREEN_H)

        # Текущее X положение на экрана
        self.px: float
        if px is not None:
            self.px = px
        else:
            self.px = randint(self.movement_rect.left, self.movement_rect.right)

        # Текущее Y положение на экрана
        self.py: float
        if py is not None:
            self.py = py
        else:
            self.py = randint(self.movement_rect.top, self.movement_rect.bottom)

        # если указано направление атаки (движения)
        self.attack_to = attack_to
        if self.attack_to is not None:
            if (self.attack_to.x is not None) and (self.attack_to.y is not None):
                self.action_move_to: bool = True
                self.move_to = Point(self.attack_to.x, self.attack_to.y)

            if self.attack_to.direction is not None:
                d = self.attack_to.direction
                self.discrete_direction = get_discrete_direction(d)  # Дискретное направление движения/стояния/ожидания в градусах
                self.direction = d
                self.action_move_to = True
                dx, dy = get_dx_dy(distance=SCREEN_W * 1.4, direction=self.direction)
                self.move_to = Point(dx, dy)

            if self.attack_to.object is not None:
                mo: MilitaryObject = self.attack_to.object
                self.action_move_to: bool = True
                self.move_to = Point(mo.px, mo.py)

        else:
            # Реальное направление движения/стояния/ожидания в градусах
            if start_direction is not None:
                d = start_direction
            else:
                d = randint(self.direction_interval.v1, self.direction_interval.v2)
            self.discrete_direction = get_discrete_direction(d)  # Дискретное направление движения/стояния/ожидания в градусах
            self.direction = d

        if start_move & (start_move_to is None):
            self.move_to = self.get_next_point_to()  # координаты точки к которой движется если self.action_move_to = True

        self.rotate_to = start_rotate_to
        if start_rotate & (start_rotate_to is None):
            self.rotate_to = self.get_next_direction_to()  # координаты точки к которой движется если self.action_move_to = True

        # Скорость движения объекта вперёд. Приращение в пикселях за фрейм прорисовки
        self.speed_move_px_frm: float
        if speed_px_sec is not None:
            self.speed_move_px_frm = speed_px_sec / FPS
        else:
            self.speed_move_px_frm = randint(self.speed_move_interval.v1, self.speed_move_interval.v2) / FPS
        # self.dx: float
        # self.dy: float
        # self.dx, self.dy = get_dx_dy(distance=self.speed_move, direction=self.direction)

        # скорость поворота в градусах за фрейм прорисовки
        self.speed_rotation_grd_frm: float
        if speed_grad_sec is not None:
            self.speed_rotation_grd_frm = speed_grad_sec / FPS
        else:
            self.speed_rotation_grd_frm = randint(self.speed_rotate_interval.v1, self.speed_rotate_interval.v2) / FPS

        # Величина жизни/здоровья
        self._hp_value: int | None = None
        if hp_value is not None:
            self.hp_value = hp_value
        else:
            self.hp_value = randint(self.hp_interval.v1, self.hp_interval.v2)
        self.hp_color = Color("green")
        self.hp_font: FontType = self.hp_font_default

        # статус для выбора последовательности картинок
        if status_start is not None:
            self._status = status_start
        else:
            self._status = MS.IDLE
        self.status_previous = self._status  # предыдущий статус объекта
        # print(f"_status: {self._status}, MS.IDLE: {MS.IDLE}, MS.MOVE_A000: {MS.MOVE_A000}")
        if self.action_move_to:
            d = get_angle(self.px, self.py, self.move_to.x, self.move_to.y)
            self.direction = d

        self.images_list: list[pygame.Surface] = self.STATUS_IMAGES.get(self.status)  # список картинок для отображения в текущем статусе изображений
        self.image_index: int = 0  # индекс картинки в текущем массиве картинок
        self.image = self.images_list[self.image_index]  # собственно сама картинка
        self.rect = self.image.get_rect()  # место фактического размещения спрайта

        # self.action_fire: bool = False
        # # self.action_fire_status = IMAGE_STATUS_FIRE  # для указания набора картинок
        # self.action_explode: bool = False  # Взрыв
        # self.action_none: bool = False  # для удаления объекта
        self.tremble_on_idle: bool = True  # Дрожать во время стоянки/ожидания
        self.body_status = BODY_SOLID  # Твёрдое тело или пустое тело, сквозь которое проходят другие объекты на экране

    # @property
    # def rect(self) -> RectType:
    #     """
    #     Место фактического размещения спрайта
    #     :return: RectType
    #     """
    #     return self.image.get_rect()  # место фактического размещения спрайта

    @property
    def parked(self) -> pygame.sprite.Sprite | None:
        return self._parked

    @parked.setter
    def parked(self, value: object | None):
        self._parked = value
        if value is not None:
            self.direction = None
            self.action_move_to = False
            self.action_rotate_to = False
            self.status = MS.IDLE

    @property
    def rotate_to(self) -> float | None:
        return self._rotate_to

    @rotate_to.setter
    def rotate_to(self, value: float | None):
        self._rotate_to = value

    @property
    def move_to(self) -> Point | None:
        return self._move_to

    @move_to.setter
    def move_to(self, point_to: Point | None):
        self.target_next_time_now = datetime.datetime.now() + timedelta(milliseconds=self.target_next_wait_ms)
        self._move_to = point_to

    @property
    def hp_value(self) -> int:
        return self._hp_value

    @hp_value.setter
    def hp_value(self, value: int):
        self._hp_value = value
        if self._hp_value <= 0:
            self.status = MS.DEAD

    def damage_to(self, point: Point | None = None, to_obj: object | None = None):
        111
        pass

    def damage_me(self, point: Point | None = None, from_obj: object | None = None):
        222
        pass

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value: int):
        if value != self._status:
            if value == MS.NONE:
                self.status_previous = self._status
                self._status = value
                self.images_list = None
                self.image = None
                self.rect = None
            else:
                if value == MS.PREV:
                    self._status = self.status_previous
                    self.status_previous = MS.IDLE
                else:
                    self.status_previous = self._status
                    self._status = value
                self.images_list = self.STATUS_IMAGES[self._status]
                self.image_index = 0
                self.image = self.images_list[self.image_index]
                self.rect = self.image.get_rect()

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value: float | None):
        if self.status in self.unrotable_statuses: return
        self._direction = value
        dd = get_discrete_direction(self._direction)
        if dd != self.discrete_direction:
            self.discrete_direction = dd
            match self.discrete_direction:
                case DIRECTION.A000:
                    self.status = MS.MOVE_A000
                case DIRECTION.A045:
                    self.status = MS.MOVE_A045
                case DIRECTION.A090:
                    self.status = MS.MOVE_A090
                case DIRECTION.A135:
                    self.status = MS.MOVE_A135
                case DIRECTION.A180:
                    self.status = MS.MOVE_A180
                case DIRECTION.A225:
                    self.status = MS.MOVE_A225
                case DIRECTION.A270:
                    self.status = MS.MOVE_A270
                case DIRECTION.A315:
                    self.status = MS.MOVE_A315
                case None:
                    pass
                case _:
                    raise Exception(F"def direction(self, value: float). Не обрабатываемое значение направления {self.discrete_direction}")
                    # GamePhase.phase = Phases.QUIT
                    # exit(10)

    def get_next_point_to(self) -> Point:
        px: float = randint(self.movement_rect.left, self.movement_rect.right)
        py: float = randint(self.movement_rect.top, self.movement_rect.bottom)
        return Point(px, py)

    @staticmethod
    def get_next_direction_to() -> float:
        d: float = randint(0, 359)
        return d

    def image_next(self):
        # now: datetime = datetime.datetime.now()
        # print("NEXT: ", self.frameTimeNext, now)
        # if self.image_step_time_next <= now:
        # self.step_time_next = now + datetime.timedelta(milliseconds=self.image_step_wait)
        now: datetime = datetime.datetime.now()
        if self.image_next_time_now <= now:
            self.image_next_time_now = now + timedelta(milliseconds=self.image_next_wait_ms)
            if (self.images_list is not None) and (len(self.images_list) > 0):
                if self.image_index < (len(self.images_list) - 1):
                    self.image_index += 1
                else:
                    if self.status in self.displayed_once.keys():
                        self.status = self.displayed_once.get(self.status)
                    else:
                        self.image_index = 0
                if self.images_list is not None:
                    self.image = self.images_list[self.image_index]
                    self.rect = self.image.get_rect()
                else:
                    self.image = None
                    self.rect = None
            else:
                self.print_error(err="MilitaryObject.image_next(): Нет списка изображений для статуса объекта " + str(self.status))
                print(self.STATUS_IMAGES)
                pass

    def has_idle(self) -> bool:
        idle: bool = self.status == MS.IDLE
        # return (not self.action_move) and (not self.action_rotate) \
        #        and (not self.controls.status_lf) and (not self.controls.status_rt) \
        #        and (not self.controls.status_fw) and (not self.controls.status_bw) \
        #        and (not self.action_move_to) \
        #        and (len(self.cmd_queue) == 0) \
        #        and (not self.action_tow_to)
        return idle

    def draw_hp(self):
        if (self.hp_value is not None) and self.hp_to_draw:  # and (self.hp_value > 0):
            t: pygame.Surface = self.hp_font.render(str(self.hp_value), ANTIALIASING, self.hp_color)
            r: RectType = t.get_rect()
            r.right = self.rect.centerx - 2
            r.bottom = self.rect.bottom
            self.screen.blit(t, r)

    def draw_title(self):
        if (self.title is not None) and self.title_to_draw:
            t: pygame.Surface = self.title_font.render(str(self.title), ANTIALIASING, self.title_color)
            r: RectType = t.get_rect()
            r.left = self.rect.centerx + 2
            r.bottom = self.rect.bottom
            self.screen.blit(t, r)

    def draw_target(self, x: float, y: float):
        if (x is not None) & (y is not None):
            # Параметры отрисовки прицела авто-движения
            TARGET_ELLIPSE_W: int = 30
            TARGET_ELLIPSE_H: int = 15
            TARGET_ELLIPSE_BORDER: int = 1
            TARGET_ELLIPSE_COLOR: Color = Color(91, 62, 0, 255)
            rect_to: RectType = RectType(x - TARGET_ELLIPSE_W / 2, y - TARGET_ELLIPSE_H / 2,
                                         TARGET_ELLIPSE_W, TARGET_ELLIPSE_H)
            pygame.draw.ellipse(self.screen, TARGET_ELLIPSE_COLOR, rect_to, TARGET_ELLIPSE_BORDER)
            pygame.draw.line(surface=self.screen, color=TARGET_ELLIPSE_COLOR,
                             start_pos=(x + TARGET_ELLIPSE_W / 4, y),
                             end_pos=(x + TARGET_ELLIPSE_W, y), width=TARGET_ELLIPSE_BORDER)
            pygame.draw.line(surface=self.screen, color=TARGET_ELLIPSE_COLOR,
                             start_pos=(x - TARGET_ELLIPSE_W / 4, y),
                             end_pos=(x - TARGET_ELLIPSE_W, y), width=TARGET_ELLIPSE_BORDER)
            pygame.draw.line(surface=self.screen, color=TARGET_ELLIPSE_COLOR,
                             start_pos=(x, y + TARGET_ELLIPSE_H / 4),
                             end_pos=(x, y + TARGET_ELLIPSE_H), width=TARGET_ELLIPSE_BORDER)
            pygame.draw.line(surface=self.screen, color=TARGET_ELLIPSE_COLOR,
                             start_pos=(x, y - TARGET_ELLIPSE_H / 4),
                             end_pos=(x, y - TARGET_ELLIPSE_H), width=TARGET_ELLIPSE_BORDER)

    def draw_cross(self):
        # крестик и эллипс для визуального контроля положения отрисовки
        # if self.parent is None:
        w100 = (self.rect.width / 2) * 1.3  # 100 радиус ширины отрисовки эллипса
        h50 = (self.rect.height / 2) * 1.3  # 50 радиус высоты отрисовки эллипса
        pygame.draw.line(surface=self.screen,
                         color=self.hairs_color,
                         start_pos=(self.px - w100, self.py),
                         end_pos=(self.px + w100, self.py))
        pygame.draw.line(surface=self.screen,
                         color=self.hairs_color,
                         start_pos=(self.px, self.py - h50),
                         end_pos=(self.px, self.py + h50))
        pygame.draw.ellipse(surface=self.screen,
                            color=self.hairs_color,
                            rect=(self.px - w100, self.py - h50, 2 * w100, 2 * h50),
                            width=1)
        if self.action_move_to:
            # линия направления движения
            d = get_distance(x1=self.px, y1=self.py, x2=self.move_to.x, y2=self.move_to.y)
            if d > 150: d = 150  # Длина линии - указателя направления движения
            dx, dy = get_dx_dy(distance=d, direction=self.direction)
            pygame.draw.line(surface=self.screen, color=self.hairs_color,
                             start_pos=(self.px, self.py), end_pos=(self.px + dx, self.py + dy))

    def draw(self):
        # позиция отрисовки изображения
        self.rect.centerx = round(self.px)
        self.rect.centery = round(self.py)

        if self.cross_draw == CROSS_DRAW.PRE:
            self.draw_cross()

        # Если установлен self.action_move_to, то рисовать цель движения
        if self.action_move_to:
            self.draw_target(self.move_to.x, self.move_to.y)

        # Дрожание когда не двигается
        if self.tremble_on_idle:
            if self.has_idle():
                seq = [-2, -1, 0, 1, 2]
                sx = choices(seq, weights=[1, 10, 1500, 10, 1], k=1)[0]
                sy = choices(seq, weights=[1, 10, 1500, 10, 1], k=1)[0]
                self.rect.x += sx
                self.rect.y += sy
        shift = self.DRAW_SHIFT.get(self.status, Delta(0, 0))
        self.rect.centerx += shift.dx
        self.rect.centery += shift.dy
        self.screen.blit(self.image, self.rect)
        self.rect.centerx -= shift.dx
        self.rect.centery -= shift.dy

        self.draw_hp()
        self.draw_title()

        if self.cross_draw == CROSS_DRAW.POST:
            self.draw_cross()

    def can_move(self, px: float, py: float) -> bool:
        """
        Проверяет можно ли переместиться в указанную точку.
        1. Если припаркован, то можно
        2. проверяет границы экрана
        3. перебирает список "своих" и "врагов", которые твёрдые и перебирает на предмет пересечения.
        Если пересекается, то False
        :param px: координаты проверяемых точек
        :param py: координаты проверяемых точек
        :return: bool: можно или нельзя перемещаться в эту точку
        """
        if self.parked is not None:
            return True
        if (px is None) or (py is None):
            return False
        can: bool = True
        r: RectType = self.rect.copy()
        r.center = round(px), round(py)

        # проверка отключена, поскольку генерация точки направления движения происходит в пределах экрана
        # и вылет за пределы экрана происходит только при поворотных манёврах
        # в пределах экрана
        # if ((r.centerx < 0)
        #         or (r.centerx > SCREEN_W)
        #         or (r.centery < 0)
        #         or (r.centery > SCREEN_H)):
        #     can = False

        # (не дочерний) и (не на буксире) и (не прозрачный)
        if self.body_status == BODY_SOLID:
            for objects in [self.yours, self.aliens]:
                for o in objects:
                    a: MilitaryObject = o
                    # это MilitaryObject
                    if isinstance(a, MilitaryObject):
                        # (проверяемый не я) и (проверяемый твердый)
                        if (self.id != a.id) and (a.body_status == BODY_SOLID):
                            # print("1: ",  self, a, self.id, a.id)
                            # если мой rect пересекается со сравниваемым rect
                            if r.colliderect(a.rect):
                                # if not ((self.id == 1 or self.id == 3) and (a.id == 1 or a.id == 3)):
                                # print("FALSE: ", self, a, self.id, a.id)
                                can = False
                                break
        # if not self.screen_rect.contains(r): can = False
        return can

    def set_direction(self, direction_to: float = None, rotate: float = None):
        """
        Устанавливает абсолютное значение угла направления
        или относительный поворот угла направления
        :param direction_to: установить направление
        :param rotate:повернуть на указанную величину
        :return: ничего не возвращает. Изменяет значение поля self.direction
        """
        # print("set_direction: ", direction_to, rotate)
        d = self.direction
        if direction_to is not None:
            d = direction_to
        if rotate is not None:
            d += rotate
        if d > 360:
            d -= 360
        if d < 0:
            d += 360
        self.direction = d

    def update_move_to(self, px: float, py: float) -> ():
        """
        Вычисление координат следующего шага из позиции px, py в направление self.move_to.
        По ходу, меняет направление движения.
        :param px: Текущая позиция
        :param py: Текущая позиция
        :return: px, py нового положения объекта
        """
        if self.target_next_time_now < datetime.datetime.now():
            self.move_to = self.get_next_point_to()
        # print("UPDATE_MOVE_TO: ", "move_to_x: ", self.move_to_x, " move_to_y: ", self.move_to_y)
        target_direction = get_angle(px, py, self.move_to.x, self.move_to.y)
        # print("UPDATE_MOVE_TO: MOVE_TO ANGLES: from: ", int(self.direction), "to: ", int(d))
        rotation_sign: int = get_rotate_direction(angle_from=self.direction, angle_to=target_direction)
        rotate_sector = get_sector(angle1=self.direction, angle2=target_direction)
        # print("UPDATE_MOVE_TO: ", "from: ", self.get_direction(), " to: ", target_direction,
        #       " sector: ", rotate_sector, rotation_sign)

        if rotate_sector < self.speed_rotation_grd_frm * 2:
            self.set_direction(direction_to=target_direction)
        else:
            self.set_direction(rotate=rotation_sign * self.speed_rotation_grd_frm)

        # if (self.rotate_and_move and (rotate_sector > self.speed_rotation_grd_frm)) or
        #    (rotate_sector < self.rotate_in_place_angle):
        if self.rotate_and_move or (rotate_sector < self.speed_rotation_grd_frm) or (rotate_sector < self.rotate_in_place_angle):
            # Чтобы поворот и движение к цели были одновременными или по очереди, сдвинуть следующий блок:
            distance = get_distance(px, py, self.move_to.x, self.move_to.y)  # дистанция до назначения сейчас
            if distance > self.speed_move_px_frm:
                dx, dy = get_dx_dy(direction=self.direction, distance=self.speed_move_px_frm)

                # Двигаться вперед только если текущее направление движения не более 45 градусов от направления назначения
                # d2 = get_distance(px + dx, py + dy, self._move_to.x, self._move_to.y)  # дистанция, которая будет после перемещения
                # if (distance - d2) > (self.speed_move * 0.71):

                if self.rotate_inertial_move:
                    px += dx
                    py += dy
                elif rotate_sector < self.rotate_in_place_angle:  # distance > d2:
                    px += dx
                    py += dy
            else:
                px = self.move_to.x
                py = self.move_to.y
                self.action_move_to = False
        return px, py

    def update_image_status(self):
        # if self.action_fire:
        #    self.image_status = IMAGE_STATUS_FIRE
        # else:
        #    self.image_status = IMAGE_STATUS_IDLE
        pass

    def update_rotate_to(self):
        direction: float = self.direction
        sector = get_sector(self.direction, self.rotate_to)
        if sector > self.speed_rotation_grd_frm:
            sign = get_rotate_direction(angle_from=self.direction, angle_to=self.rotate_to)
            direction += sign * self.speed_rotation_grd_frm
        else:
            direction = self.rotate_to
            self.action_rotate_to = False
        return direction

    # def update_queue(self):
    #     cmd: Cmd = self.cmd_queue[0]
    #     # если ожидающего актёра нет ИЛИ ожидающий актёр указан и он без очереди команд
    #     if (cmd.when_actor_idle is None) or \
    #             ((cmd.when_actor_idle is not None) and cmd.when_actor_idle.has_idle()):
    #         if cmd.id == CMD_TOW:
    #             # print(f"1: {self.title}[{self.id}] => {cmd.slot.parent.title}[{cmd.slot.parent.id}] ")
    #             self.mount_to(to_parent=cmd.slot)
    #             self.cmd_queue.__delitem__(0)
    #             del cmd

    def update_search_parking(self):
        global ACTORS
        a: MilitaryObject
        for a in ACTORS:
            if (a.id != self.id) and a.parking_place:
                if a in self.parkings:
                    d: float = get_distance(self.px, self.py, a.px, a.py)
                    if d <= self.parkings_distance:
                        if d <= self.speed_move_px_frm:
                            self.parked = a
                        else:
                            self.move_to_set(point=Point(a.px, a.py))

    def fire(self, target: object):
        print("FIRE")
        pass

    def update_status_fire(self, on: bool, to: Point):
        d = get_discrete_direction(get_angle(x1=self.px, y1=self.py, x2=to.x, y2=to.y))
        if on:
            match d:
                case DIRECTION.A000:
                    self.status = MS.FIRE_A000
                case DIRECTION.A045:
                    self.status = MS.FIRE_A045
                case DIRECTION.A090:
                    self.status = MS.FIRE_A090
                case DIRECTION.A135:
                    self.status = MS.FIRE_A135
                case DIRECTION.A180:
                    self.status = MS.FIRE_A180
                case DIRECTION.A225:
                    self.status = MS.FIRE_A225
                case DIRECTION.A270:
                    self.status = MS.FIRE_A270
                case DIRECTION.A315:
                    self.status = MS.FIRE_A315
                case _:
                     exit("update_status_fire: Этого не должно быть(1)")
        else:
            match d:
                case DIRECTION.A000:
                    self.status = MS.MOVE_A000
                case DIRECTION.A045:
                    self.status = MS.MOVE_A045
                case DIRECTION.A090:
                    self.status = MS.MOVE_A090
                case DIRECTION.A135:
                    self.status = MS.MOVE_A135
                case DIRECTION.A180:
                    self.status = MS.MOVE_A180
                case DIRECTION.A225:
                    self.status = MS.MOVE_A225
                case DIRECTION.A270:
                    self.status = MS.MOVE_A270
                case DIRECTION.A315:
                    self.status = MS.MOVE_A315
                case _:
                     exit("update_status_fire: Этого не должно быть(2)")


    def update_search_aliens(self):
        global ACTORS
        current_time = datetime.datetime.now()
        if current_time >= self.recharge_time_now:
            self.recharge_time_now = current_time + timedelta(milliseconds=self.recharge_wait_ms)  # время готовности к выстрелу
            if len(self.aliens) > 0:
                a: MilitaryObject
                for a in ACTORS:
                    if a.id != self.id:
                        if a in self.aliens:
                            d: float = get_distance(self.px, self.py, a.px, a.py)
                            if d <= self.aliens_distance:
                                self.update_status_fire(True, Point(a.px, a.py))
                                self.fire(a)
                            else:
                                self.update_status_fire(False, self.move_to)

    def update(self):
        px: float = self.px
        py: float = self.py

        if (self.attack_to is not None) and (self.attack_to.object is not None):
            mo: MilitaryObject = self.attack_to.object
            # print(mo.title, mo.px, mo.py)
            self.move_to = Point(mo.px, mo.py)
            px, py = self.update_move_to(px=px, py=py)

        if self.parked is not None:
            p: MilitaryObject = self.parked
            px = p.px
            py = p.py

        else:
            # Поиск парковок
            if self.parkable:
                self.update_search_parking()
            # Поиск врагов
            self.update_search_aliens()
            # Вращение
            if self.action_rotate_to:
                self.set_direction(direction_to=self.update_rotate_to())
            # MOVE_TO
            if self.action_move_to:
                px, py = self.update_move_to(px=px, py=py)

        # Если в это место можно перемещаться, то перемещаемся
        if self.can_move(px=px, py=py):
            self.px = px
            self.py = py

        """
        if self.controls.status_uc:
            d = get_discrete_direction(self.get_direction())
            self.DRAW_SHIFT[d] = Delta(dx=self.DRAW_SHIFT.get(d).dx, dy=self.DRAW_SHIFT.get(d).dy - 1)
        if self.controls.status_dc:
            d = get_discrete_direction(self.get_direction())
            self.DRAW_SHIFT[d] = Delta(dx=self.DRAW_SHIFT.get(d).dx, dy=self.DRAW_SHIFT.get(d).dy + 1)
        if self.controls.status_rc:
            d = get_discrete_direction(self.get_direction())
            self.DRAW_SHIFT[d] = Delta(dx=self.DRAW_SHIFT.get(d).dx + 1, dy=self.DRAW_SHIFT.get(d).dy)
        if self.controls.status_lc:
            d = get_discrete_direction(self.get_direction())
            self.DRAW_SHIFT[d] = Delta(dx=self.DRAW_SHIFT.get(d).dx - 1, dy=self.DRAW_SHIFT.get(d).dy)
        if self.controls.status_fire:
            print("---------------------------------------")
            print("DRAW_SHIFT: ",  self.DRAW_SHIFT)
            print("---------------------------------------")
        """

        self.image_next()

    def event_handler(self, event: EventType):
        # self.controls.event_handler(event=event)
        # if len(self.slots) > 0:
        #     s: Slot
        #     for s in self.slots:
        #         s.event_handler(event=event)
        pass

    error_already_printed = ""  # Уже выведенное сообщение об ошибке

    def print_error(self, prefix="ERROR: ", err="", print_one: bool = True):
        if print_one and (self.error_already_printed == err):
            pass
        else:
            print(self.title, ": ", prefix, err)
            self.error_already_printed = err

    def move_to_set(self, point: Point | None = None, delta: Delta | None = None):
        if point is not None:
            self.move_to = point
        if delta is not None:
            self.move_to = Point(x=self.px + delta.dx, y=self.py + delta.dy)
        self.action_move_to = True
        self.action_rotate_to = False
        # self.action_move = False
        # self.action_rotate = False
        # self.action_fire = False
        # self.action_jump = False

    def rotate_to_set(self, direction_to: float = None):
        if direction_to is not None:
            self.rotate_to = direction_to
        self.action_rotate_to = True
        self.action_move_to = False
        # self.action_move = False
        # self.action_rotate = False
        # self.action_fire = False
        # self.action_jump = False


MilitaryObjectType = MilitaryObject


# --------------------------------------------------------------
# Процедуры массового управления объектами класса MilitaryObject
# --------------------------------------------------------------


# def events():  # actors: list[MilitaryObject]
#     global ACTORS
#     event: EventType
#     for event in pygame.event.get():
#         i: MilitaryObject
#         for i in ACTORS:
#             i.event_handler(event)
#         if (event.type == pygame.QUIT) or (
#                 event.type == pygame.KEYDOWN and event.key == pygame.K_BACKQUOTE):  # K_ESCAPE
#             sys.exit()
#         # if event.type == pygame.KEYDOWN:
#         #     print("KEY: ", event.key)
#         # if event.type == pygame.MOUSEBUTTONDOWN:
#         #     print("BTN: ", event.pos, event.button)
#         # if event.type == pygame.MOUSEMOTION:
#         #     print("MOV: ", event.pos)


def update():  # actors: list[MilitaryObject]
    """Обновление параметров объектов"""
    global ACTORS
    i: MilitaryObject
    for i in ACTORS:
        i.update()
        if isinstance(i, MilitaryObject) and i.status == MS.NONE:
            # print(f"ID: {i.title}[{i.id}] Удаление объекта.")
            ACTORS.remove(i)
            del i
            # print(f"Осталось: {len(ACTORS)}")


def draw(display_flip: bool = False):  # actors: list[MilitaryObject]
    """Отрисовка объектов на экране"""
    global ACTORS
    i: MilitaryObject
    for i in ACTORS:
        i.draw()
    if display_flip:
        pygame.display.flip()


def run_step():  # actors: list[MilitaryObject]
    update()
    draw()

# def run():  # actors: list[MilitaryObject]
#     global ACTORS
#     global TIME_DRAW_FRAME
#     while True:
#         now: datetime = datetime.datetime.now()
#         if TIME_DRAW_FRAME <= now:
#             TIME_DRAW_FRAME = now + datetime.timedelta(milliseconds=TIME_WAITING)
#             events(actors=actors)
#             update(actors=actors)
#             draw(actors=actors)
#             # if not kv.action_move_to and m_index < len(m):
#             #     kv.move_to(dx=m[m_index][0], dy=m[m_index][1])
#             #     m_index += 1
#
#             # print(TIME_DRAW_FRAME)
#             # pass
#             # break
