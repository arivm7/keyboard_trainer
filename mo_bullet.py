import datetime
import random
import pygame
from pygame.draw_py import Point
from pygame.rect import RectType

from globals import SCREEN, compare_float
from military_object import MilitaryObject, Interval, CROSS_DRAW, MS, AttackTo

img_bullet = pygame.image.load("img/bullet/yadro15.png")


class Bullet(MilitaryObject):

    title: str = "Bullet"
    title_to_draw: bool = False  # выводить на экран название
    hp_to_draw: bool = False  # выводить на экран hp

    cross_draw = CROSS_DRAW.OFF  # Крестик положения, эллипс размера и линия направления движения
    speed_move_interval: Interval = Interval(90, 180)  # Интервал автоматического назначения скорости движения
    hp_interval: Interval = Interval(50, 80)  # Интервал автоматического назначения hp

    STATUS_IMAGES = {
        # MS.IDLE: list,  # pygame.Surface
        # MS.DEAD: list,  # pygame.Surface
        MS.FLY: [img_bullet],
        MS.EXPLODE: [
            pygame.image.load("img/explode/01/050/01_01.png"),
            pygame.image.load("img/explode/01/050/01_02.png"),
            pygame.image.load("img/explode/01/050/01_03.png"),
            pygame.image.load("img/explode/01/050/01_04.png"),
            pygame.image.load("img/explode/01/050/01_05.png"),
            pygame.image.load("img/explode/01/050/01_06.png"),
            pygame.image.load("img/explode/01/050/01_07.png"),
            pygame.image.load("img/explode/02/050/02_01.png"),
            pygame.image.load("img/explode/02/050/02_02.png"),
            pygame.image.load("img/explode/02/050/02_03.png"),
            pygame.image.load("img/explode/02/050/02_04.png"),
            pygame.image.load("img/explode/02/050/02_05.png"),
            pygame.image.load("img/explode/02/050/02_06.png"),
            pygame.image.load("img/explode/02/050/02_07.png"),
            pygame.image.load("img/explode/02/050/02_08.png"),
            pygame.image.load("img/explode/02/050/02_09.png"),
        ],
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
        MS.MOVE_RC: [img_bullet],
        MS.MOVE_RD: [img_bullet],
        MS.MOVE_DC: [img_bullet],
        MS.MOVE_LD: [img_bullet],
        MS.MOVE_LC: [img_bullet],
        MS.MOVE_LU: [img_bullet],
        MS.MOVE_UC: [img_bullet],
        MS.MOVE_RU: [img_bullet]
    }

    # MS-Статусы, которые выполняются один раз,
    # за тем статус меняется на указанный
    displayed_once = {
        MS.EXPLODE: MS.NONE
    }

    def __init__(self,
                 start_from: Point,  # координаты точки из которой движется
                 attack_to: AttackTo,
                 speed_px_sec: float = None,  # пикселей в секунду
                 speed_grad_sec: float = None,  # градусов в секунду
                 hp_value: int = None,  # величина здоровья/жизни
                 start_direction: float = None,
                 status_start: int = MS.FLY,  # Стартовый статус
                 screen: pygame.Surface = SCREEN):
        super().__init__(px=start_from.x, py=start_from.y,
                         attack_to=attack_to,
                         start_direction=start_direction,
                         speed_px_sec=speed_px_sec,
                         speed_grad_sec=speed_grad_sec,
                         hp_value=hp_value,
                         status_start=status_start,
                         screen=screen)

    def update_move_to(self, px: float, py: float):
        px, py = super().update_move_to(px=px, py=py)
        if (compare_float(px, self.move_to.x) == 0) and (compare_float(py, self.move_to.y) == 0):
            self.status = MS.EXPLODE
        return px, py
