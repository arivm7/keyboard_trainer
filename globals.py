import json
import os
from collections import namedtuple
from operator import countOf

import pygame
from datetime import datetime, timedelta
from enum import Enum
from math import degrees, atan, radians, cos, sin, acos
from pygame import Color
from pygame.event import EventType
from pygame.rect import RectType

CONF_LESSONS = 'conf.json'
SAVE_DIR = 'saves'
BOOKS_DIR = "books"
USER_FILE_PREFIX = 'GAMER_'
USER_FILE_SUFFIX = '.json'
MAX_LESSON_STR = 'йцукенгшщзхъ\\ фывапролджэ ячсмитьбю. ё1234567890-='
MAX_LESSON_LEN = len(MAX_LESSON_STR)
SEVERITY_ERRORS: int = 10  # Коэффициент снижения скорости для ошибочных кнопок
# REGENERATE_STR = True  # Всегда перегенерировать строку урока на основании generate_str. Строка fixed_str неизменна.

FromTo = namedtuple('FromTo', ['f', 't'])

ALL_WORDS: dict = {}  # Набор слов для генерации уроков
COUNT_WORDSET_FOR_USE_WEIGHT: int = 2000  # Длина набора слов, после которой использовать вес_слов
WORD_LENGTH: FromTo = FromTo(2, 10)  # Диапазон длин слов для выборки для уроков

APP_TITLE: str = "Клавиатурный тренажёр"
SCREEN_W: int = 1024  # Размер экрана
SCREEN_H: int = 768 - 20  # Размер экрана

pygame.init()
SCREEN: pygame.Surface = pygame.display.set_mode(size=(SCREEN_W, SCREEN_H))
pygame.display.set_caption(APP_TITLE)
FPS: int = 60
TIME_WAITING: int = int(1000 / FPS)
TIME_DRAW_FRAME: datetime = datetime.now() + timedelta(milliseconds=TIME_WAITING)

KEYBOARD_HEIGHT = 283  # SCREEN_H - 450  # 375 -- это высота клавиатуры
WORK_RECT: pygame.Rect = pygame.rect.Rect(0, 0, SCREEN_W, SCREEN_H - KEYBOARD_HEIGHT)
MARGIN_W: int = int(SCREEN_W / 6)
MARGIN_H: int = int(MARGIN_W / 3)
LINE_Y: int = WORK_RECT.bottom - MARGIN_H  # линия движения символов
LINE_X1: int = MARGIN_H
LINE_X2: int = SCREEN_W - MARGIN_H
LINE_RECT = pygame.rect.Rect(MARGIN_W, MARGIN_H, SCREEN_W - MARGIN_W * 2, LINE_Y - MARGIN_H * 2)
# print(f"LINE_X1: {LINE_X1} | LINE_Y: {LINE_Y} | LINE_RECT: {LINE_RECT}")
SPEED_LPM: int = 200  # LPM letters / min
TIME_ONE_LETTER = SPEED_LPM / 60
ACCURACY: int = 1000  # Точность для сравнения float

pygame.font.init()


def get_font_default(font_name: str = None, font_size: int = 38) -> pygame.font.Font:
    return pygame.font.Font(font_name, font_size)


FONT_DEFAULT = get_font_default(None, 38)
ANTIALIASING = True  # 1 -- если поддерживается сглаживание, 0 -- если не поддерживается
CHAR_WIDTH: int = 28
CHAR_HEIGHT: int = 34
# CHAR_SPACING_COEFFICIENT: float = 1.5
CHAR_SPACING: float = CHAR_WIDTH * 0.15

KB_LAYOUT_EN: int = 1
KB_LAYOUT_RU: int = 2
KB_LAYOUT_UA: int = 3


class COLOR:
    BK: Color = Color(10, 10, 10, 255)
    TEXT_DEFAULT: Color = Color(20, 180, 130, 255)
    BK_DEFAULT: Color = Color(20, 20, 20, 255)
    QUEUE: Color = Color(10, 52, 123, 255)
    CURRENT: Color = Color(10, 107, 123, 255)
    UNDERLINE: Color = Color(10, 107, 123, 255)
    RED: Color = Color(150, 10, 10, 255)
    YELLOW: Color = Color(200, 200, 20, 255)
    FAIL: Color = Color(50, 50, 50, 255)
    GREEN: Color = Color(20, 180, 30, 255)
    SUCCESS: Color = Color(20, 50, 30, 255)
    BLACK90: Color = Color(25, 25, 25, 255)
    BLACK80: Color = Color(51, 51, 51, 255)
    BLACK60: Color = Color(102, 102, 102, 255)
    BLACK40: Color = Color(153, 153, 153, 255)
    BLACK20: Color = Color(204, 204, 204, 255)
    BLUE: Color = Color(25, 25, 230, 255)
    HELP_KEY: Color = Color(204, 204, 26, 255)
    HELP_WORD: Color = Color(204, 156, 26, 255)
    LABEL: Color = Color(13, 64, 8, 255)
    NAME: Color = Color(12, 128, 8, 255)
    CURSOR: Color = Color(125, 122, 0, 255)
    MENU: Color = Color(179, 179, 51, 255)
    MENU_TEXT: Color = Color(12, 70, 20, 255)
    MENU_TEXT_SELECTED: Color = Color(65, 70, 12, 255)
    MENU_BK: Color = Color(0, 30, 20, 255)
    MENU_BK_SELECTED: Color = Color(45, 47, 26, 255)
    MENU_BORDER: Color = Color(150, 80, 10, 255)
    MENU_RATING: Color = Color(179, 179, 128, 255)
    BORDER_ACTIVE: Color = Color(20, 200, 225, 255)
    BORDER_PASSIVE: Color = Color(20, 60, 60, 255)


_ID: int = 1000


def auto_id() -> int:
    """
    Возвращает следующее целое число.
    Для уникальных ID
    :rtype: object
    :return: целое число
    """
    global _ID
    _ID += 1
    return _ID


class ALIGN:
    LEFT: int = auto_id()
    CENTER: int = auto_id()
    RIGHT: int = auto_id()
    TOP: int = auto_id()
    BOTTOM: int = auto_id()


CONSOLE_COLORS = {
    # https://www.shellhacks.com/bash-colors/
    'bold': {True: '\x1b[1m', False: '\x1b[22m'},
    'cyan': {True: '\x1b[36m', False: '\x1b[39m'},
    'blue': {True: '\x1b[34m', False: '\x1b[39m'},
    'red': {True: '\x1b[31m', False: '\x1b[39m'},
    'magenta': {True: '\x1b[35m', False: '\x1b[39m'},
    'green': {True: '\x1b[32m', False: '\x1b[39m'},
    'underline': {True: '\x1b[4m', False: '\x1b[24m'},
    'dark_gray': {True: '\x1b[1;30m', False: '\x1b[0m'},
    'light_gray': {True: '\x1b[37m', False: '\x1b[0m'},
}


def print_color(text: str, console_color: CONSOLE_COLORS):
    # color = CONSOLE_COLORS['dark_gray']
    print(f"({console_color[True]}){text}({console_color[False]})")


class PHASE_RESULT(Enum):
    PREV = -1
    EXIT = 0
    NEXT = 1


class Phases:
    INTRO_0: int = auto_id()  # Сцена рассказывающая о результатах тренировок
    USER_NAME: int = auto_id()  # Сцена выбора имени игрока и загрузка сохраненной игры, если есть.
    CHOOSE_LESSONS: int = auto_id()  # Сцена выбора уроков для тренировки
    INTRO_1: int = auto_id()  # Сцена "Расположите пальцы на кнопках"
    INTRO_2: int = auto_id()  # Сцена "Приготовьтесь, нажмите любую кнопку для начала игры"
    GAME_RUN: int = auto_id()  # Сцена самой игры
    # GAME_PRE_RUN: int = auto_id()     # Сцена счетчика перед началом игры. Реализована в виде вызываемой функции перед началом урока
    GAME_RESULT: int = auto_id()  # Сцена показывающая результат игры, сохранение результатов игры
    GAME_END: int = auto_id()  # Сцена завершения игры
    GAME_NONE: int = auto_id()  # Нормальное завершение программы
    QUIT: int = auto_id()  # Выход из программы
    PRE: int = auto_id()  # фаза отрисовки предварительная (фон)
    MID: int = auto_id()  # фаза отрисовки средняя часть
    POST: int = auto_id()  # фаза отрисовки верхняя часть (надписи)

    phase: int  # Текущая фаза игры

    sequence: list = [
        GAME_END,  # Сцена завершения игры
        INTRO_0,  # Сцена рассказывающая о результатах тренировок
        USER_NAME,  # Сцена выбора имени игрока и загрузка сохраненной игры, если есть.
        CHOOSE_LESSONS,  # Сцена выбора уроков для тренировки
        INTRO_1,  # Сцена "Расположите пальцы на кнопках"
        INTRO_2,  # Сцена "Приготовьтесь, нажмите любую кнопку для начала игры"
        GAME_RUN,  # Сцена самой игры
        GAME_RESULT,  # Сцена показывающая результат игры
        GAME_END,  # Сцена завершения игры
        GAME_NONE  # Нормальное завершение программы
    ]

    def __init__(self):
        self.set_first()

    def set_first(self):
        self.phase = self.sequence[0]

    def shift_next(self):
        index = self.sequence.index(self.phase)
        if index < (len(self.sequence) - 1):
            self.phase = self.sequence[index + 1]
        else:
            self.phase = self.QUIT

    def shift_prev(self):
        index = self.sequence.index(self.phase)
        if index > 0:
            self.phase = self.sequence[index - 1]
        else:
            self.phase = self.QUIT

    def shift_phase(self, phase_result: PHASE_RESULT):
        match phase_result:
            case PHASE_RESULT.PREV:
                self.shift_prev()
            case PHASE_RESULT.NEXT:
                self.shift_next()
            case _:
                self.phase = self.QUIT


GamePhase = Phases()


class STATUS:
    INIT = auto_id()
    QUEUE = auto_id()
    ACTIVE = auto_id()
    PASSIVE = auto_id()
    PRESSED = auto_id()
    SUCCESS = auto_id()
    RED_LINE = auto_id()
    FAILED = auto_id()
    FIRED = auto_id()
    RESULT = auto_id()
    END = auto_id()
    NONE = auto_id()


class ACTION:
    move_up = auto_id()
    move_down = auto_id()
    move_home = auto_id()
    move_pg_up = auto_id()
    move_pg_down = auto_id()
    move_end = auto_id()
    move_left = auto_id()
    move_right = auto_id()
    change_state = auto_id()
    act_end = auto_id()
    act_escape = auto_id()


KEYS_SHIFT = [1073742049, 1073742053, pygame.KMOD_SHIFT, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.KMOD_LSHIFT,
              pygame.KMOD_RSHIFT]
KEYS_ALT = [1073742050, 1073742054]
KEYS_CTRL = [1073742050, 1073742054]
KEYS_ENTER = [1073741912, 1073742051]
KEYS_WIN = [1073741912, 1073742051]
KEYS_MENU = [1073741942]
KEYS_FN = []

# KEY_DOWN
# KEY_UP
# KEY_NONE


# 600 ms
# AUTO_REPEAT_WAIT: datetime = datetime(year=0, month=0, day=0, hour=0, minute=0, second=0, microsecond=600)  # 600 ms
AUTO_REPEAT_WAIT = timedelta(milliseconds=600)  # 600 ms
# интервал между повторами ввода символа. 25 -- char per seconds
# 1000 / 25 ms
# AUTO_REPEAT_ON: datetime = datetime(year=0, month=0, day=0, hour=0, minute=0, second=0, microsecond=int(1000 / 25))
AUTO_REPEAT_ON = timedelta(milliseconds=int(50))  # 1000 / 25 ms


# class CharStatus(Enum):
#     CHAR_STATUS_QUEUE = 1  # В очереди
#     CHAR_STATUS_WAITING = 2  # Ожидает нажатия кнопки
#     CHAR_STATUS_PRESSED = 3  # Кнопка нажата
#     CHAR_STATUS_NONE = 4  # Удаление картинки кнопки

# CharStatus = Enum('CharStatus', [
#     'CHAR_STATUS_QUEUE',
#     'CHAR_STATUS_WAITING',
#     'CHAR_STATUS_PRESSED',
#     'CHAR_STATUS_NONE'])

#
# ###############################################################################
#


# HP_STATUS_NONE = 0
# HP_STATUS_NORMAL = 1
# HP_STATUS_DEAD = 2
#
# CMD_MOVE_TO = 1  # Двигаться к
# CMD_ROTATE_TO = 2  # Вращаться к
# CMD_ATTACK_TO = 3  # Атаковать к (двигаться в режиме атаки)
# CMD_FIRE_IT = 4  # Стрелять в направлении
# CMD_ATTACK_IT = 5  # Стрелять в объект
# CMD_HUNT_IT = 6  # Охотитьс яза объектом
# CMD_TOW = 7  # Буксировать
#
# Cmd = namedtuple('Cmd', ['id', 'px', 'py', 'direction', 'distance', 'slot', 'when_actor_idle'],  # , 'tow_his'
#                  defaults=[None, None, None, None, None, None, None])
#
# # Параметры отрисовки прицела автодижения
# TARGET_ELLIPSE_W: int = 30
# TARGET_ELLIPSE_H: int = 15
# TARGET_ELLIPSE_BORDER: int = 1
# TARGET_ELLIPSE_COLOR: Color = Color(91, 62, 0, 255)
# #
#
#
#
#
# IMAGE_STATUS_IDLE = 1000
# IMAGE_STATUS_FIRE = 1001
# IMAGE_STATUS_JUMP = 1002
# IMAGE_STATUS_DEAD = 1003
#
#
# IMAGE_STATUS_MOVE_RC = DIRECTION_RC
# IMAGE_STATUS_MOVE_RD = DIRECTION_RD
# IMAGE_STATUS_MOVE_DC = DIRECTION_DC
# IMAGE_STATUS_MOVE_LD = DIRECTION_LD
# IMAGE_STATUS_MOVE_LC = DIRECTION_LC
# IMAGE_STATUS_MOVE_LU = DIRECTION_LU
# IMAGE_STATUS_MOVE_UC = DIRECTION_UC
# IMAGE_STATUS_MOVE_RU = DIRECTION_RU
#
# # BODY MODE STATUS
# BODY_SOLID = 1  # Твёрдое тело
# BODY_SOFT = 2  # Мягкое тело, через него проходят другие объекты на экране
#
# # MOVE MODE
# MOVE_ON_GROUND = 0b100000  # Движется по земле
# MOVE_ON_AIR = 0b010000  # Движется по воздуху
#
# Delta = namedtuple('Delta', ['dx', 'dy'])

def str_to_paragraph(long_str: str, font: pygame.font = FONT_DEFAULT, rect: pygame.Rect = LINE_RECT):
    paragraph: list[str] = []
    one_word: str = ""
    one_line: str = ""
    for c in long_str:
        if c != " ":
            one_word = one_word + c
        else:
            if font.render(one_line + " " + one_word, ANTIALIASING, COLOR.RED).get_rect().width <= rect.width:
                one_line = one_line + " " + one_word
                one_word = ""
            else:
                paragraph.append(one_line)
                one_line = one_word
                one_word = ""
    if len(one_word) > 0:
        if font.render(one_line + " " + one_word, ANTIALIASING, COLOR.RED).get_rect().width <= rect.width:
            one_line = one_line + " " + one_word
            one_word = ""
        else:
            paragraph.append(one_line)
            one_line = one_word
            one_word = ""
        # if "От 300 до 400" in long_str:
        #     print(f"line: {one_line}, word: {one_word}")
    if len(one_line) > 0:
        paragraph.append(one_line)
    return paragraph


def draw_paragraph(paragraph: list[str],
                   color: Color = COLOR.RED,
                   rect: RectType = LINE_RECT,
                   font: pygame.font = FONT_DEFAULT):
    px = rect.centerx
    i = font.render(str(paragraph[0]), ANTIALIASING, color)
    h = i.get_rect().height * 1.15
    py = rect.centery - (len(paragraph) / 2) * h + h / 2
    for s in paragraph:
        i = font.render(str(s), ANTIALIASING, color)
        r = i.get_rect()
        r.center = (px, py)
        SCREEN.blit(i, r)
        py += h


def check_quit(event: EventType):
    return (event.type == pygame.QUIT) or (
            event.type == pygame.KEYDOWN and
            (event.key == pygame.K_ESCAPE))


def time_to_draw_screen() -> bool:
    """
    Если текущее время больше или равно TIME_DRAW_FRAME,
    то TIME_DRAW_FRAME устанавливает в новое время отрисовки = сейчас + TIME_WAITING
    и возвращает True.
    Если текущее время меньше TIME_DRAW_FRAME, то просто возвращает False.
    return: bool
    """
    global TIME_DRAW_FRAME, TIME_WAITING
    now: datetime = datetime.now()
    if TIME_DRAW_FRAME <= now:
        TIME_DRAW_FRAME = now + timedelta(milliseconds=TIME_WAITING)
        return True
    else:
        return False


def get_PPD(distance: float) -> float:  # pixel per draw screen
    PPS = distance  # pixels per sec
    PPD = PPS / FPS  # pixels per one draw screen
    return PPD


def compare_float(f1: float, f2: float) -> int:
    i1 = int(f1 * ACCURACY)
    i2 = int(f2 * ACCURACY)
    if i1 > i1:
        return 1
    elif i1 < i2:
        return -1
    else:
        return 0


def get_dx_dy(distance: float, direction: float) -> ():
    """
    Возвращает приращение координат для перемещения на указанное количество пикселей в указанном направлении
    :param distance:
    :param direction:
    :return:
    """
    dx: float = cos(radians(direction)) * distance
    dy: float = sin(radians(direction)) * distance
    # print(R, a, dx, dy)
    return dx, dy


def get_distance(x1: float, y1: float, x2: float, y2: float):
    dx = x2 - x1
    dy = y2 - y1
    distance = (dx ** 2 + dy ** 2) ** 0.5
    return distance


def get_angle(x1: float, y1: float, x2: float, y2: float):
    """
    Расчёт угла через косинус-арккосинус.
    Возвращает угол в градусах направления.
    Считает через арккосинус
    0 от право-центр и по часовой стрелке до 360 градусов
    :param x1: первая точка отрезка
    :param y1:
    :param x2: вторая точка отрезка
    :param y2:
    :return:  угол отрезка в градусах
    """
    dx = x2 - x1
    dy = y2 - y1
    length = (dx ** 2 + dy ** 2) ** 0.5
    if int(length * ACCURACY) == 0:
        cos_a = 1
    else:
        cos_a = dx / length
    alpha = degrees(acos(cos_a))
    if dy < 0:
        alpha = -alpha
    if alpha < 0:
        alpha += 360
    return alpha


def set_angle(start: float, rotate: float = None):
    a: float = start
    if rotate is not None:
        a += rotate
    if a > 360:
        a -= 360
    elif a < 0:
        a += 360
    return a


def get_angle_tg(x1: float, y1: float, x2: float, y2: float):
    """
    Расчёт угла через арктангенс.
    Возвращает угол в градусах направления.
    Считает через арктангенс
    0 от право-центр и по часовой стрелке до 360 градусов
    :param x1: первая точка отрезка
    :param y1:
    :param x2: вторая точка отрезка
    :param y2:
    :return: угол направления отрезка в градусах
    """
    dx: float = x2 - x1
    dy: float = y2 - y1
    a: float
    if int(dx * ACCURACY) == 0:  # dx == 0
        if dy > 0:
            a = 90
        else:
            a = 270
    else:
        if int(dy * ACCURACY) == 0:  # dy == 0
            if dx > 0:
                a = 0
            else:
                a = 180
        else:
            a = degrees(atan(dy / dx))
    if dx < 0:
        a += 180
    if a < 0:
        a += 360
    return a


def in_sector(angle_in: float, sector_from: float, sector_to: float):
    if sector_from < sector_to:
        return int(sector_from * ACCURACY) <= int(angle_in * ACCURACY) <= int(sector_to * ACCURACY)
    else:
        # print("  ", angle1, angle, angle2)
        return (sector_from <= angle_in <= 360) or (0 <= angle_in <= sector_to)


# получает на вход два угла
# возвращает угол сектора между входящими углами
def get_sector(angle1: float | None, angle2: float | None) -> float:
    if (angle1 is None) or (angle2 is None):
        return 0.0
    sector: float = abs(angle2 - angle1)
    if sector > 180:
        sector -= 360
    return abs(sector)


def get_rotate_direction(angle_from: float, angle_to: float) -> int:
    """
    На вход получает начальный и конечный угол,
    возвращает -1, 0, +1 -- направление приращения угла для поворота.
    :param angle_from: Текущий угол направления объекта
    :param angle_to: Угол на который нужно повернуть
    :return: -1, 0, +1 -- Знак направления поворота
    """
    if ((angle_from is None) or (angle_to is None)) or (int(angle_from * ACCURACY) == int(angle_to * ACCURACY)):
        return 0
    angle_rotate: float = get_sector(angle_from, angle_to) / 10
    sector_minus: float = get_sector(angle1=angle_from, angle2=angle_to - angle_rotate)
    sector_plus: float = get_sector(angle1=angle_from, angle2=angle_to + angle_rotate)
    if sector_minus < sector_plus:
        return 1
    else:
        return -1


# Возвращает коэффициент масштабирования в зависимости от положения точки
# относительно двух базовых уровней масштабирования
#
# ---- py -- положение объекта
# ---- Yt-уровень масштабирования (например 0,75)
# ---- py -- положение объекта
# ---- Y0-уровень базового масштабирования (обычно 1,0)
# ---- py -- положение объекта
# def get_scale(py: int):
#     k: float = (SCALE_1_COEFFICIENT - SCALE_TOP_COEFFICIENT) / (SCALE_1_LINE - SCALE_TOP_LINE)
#     scale: float = k * (py - SCALE_1_LINE) + SCALE_1_COEFFICIENT
#     return scale


def read_file(file_name: str) -> str | None:
    """
    Читает файл в кодировке utf-8 в строковую переменную. Возвращает строку.
    Если ошибка чтения файла, то возвращает None
    :param file_name: str -- имя файла
    :return: str | None -- Считанный фал или None
    """
    try:
        f = open(file=file_name, mode='r', encoding='utf-8')
        c: str = f.read()
        f.close()
        return c
    except OSError as err:
        print("OS error: {0}".format(err))
        return None


def read_conf(conf_file: str):
    return json.loads(read_file(conf_file))


def read_words_dict(filename: str) -> dict | None:
    """
    Читает файл со словарем слов
    :param filename: имя файла словаря
    :return: dict -- словарь
    """
    if os.access(filename, os.F_OK):  # Check access with os.F_OK
        if os.access(filename, os.R_OK):  # Check access with os.R_OK
            f = open(file=filename, mode='r', encoding='utf-8')
            words: dict = json.loads(f.read())
            f.close()
            return words
        else:
            print("Нет доступа к файлу для чтения:", os.getcwd(), filename)
    else:
        print("Файл не найден: ", os.getcwd(), filename)
    return None


def read_user_data(username: str) -> list | None:
    """
    Читает конфиг и сохраненные данные пользователя
    :param username: имя пользователя
    :return: Конфиг + уроки
    """
    os.chdir(SAVE_DIR)
    filename = get_filename_from_username(username=username)
    if os.access(filename, os.F_OK):  # Check access with os.F_OK
        if os.access(filename, os.R_OK):  # Check access with os.R_OK
            f = open(file=filename, mode='r', encoding='utf-8')
            lessons = json.loads(f.read())
            f.close()
            os.chdir("..")
            return lessons
        else:
            print("Нет доступа к файлу для чтения:", os.getcwd(), filename)
    else:
        print("Файл не найден: ", os.getcwd(), filename)
    os.chdir("..")
    return None


def save_user_data(username: str, conf: list):
    for lesson in conf["lessons"]:
        if "img_name" in lesson:          lesson.pop("img_name")
        if "img_rating" in lesson:        lesson.pop("img_rating")
        if "img_speed" in lesson:         lesson.pop("img_speed")
        if "img_probes" in lesson:        lesson.pop("img_probes")
        # if lessons["REGENERATE_STR"]:   lesson.pop("str")
    os.chdir(SAVE_DIR)
    with open(USER_FILE_PREFIX + username + USER_FILE_SUFFIX, 'w', encoding='utf-8') as outfile:
        json.dump(conf, outfile, indent=2, ensure_ascii=False)
    os.chdir("..")


def get_username_from_filename(filename: str) -> str:
    return filename[len(USER_FILE_PREFIX):len(filename) - len(USER_FILE_SUFFIX)]


def get_filename_from_username(username: str) -> str:
    return USER_FILE_PREFIX + username + USER_FILE_SUFFIX


def count_chars(s: str) -> int:
    """
    Возвращает количество используемых отдельных символов в строке,
    без учета повторений
    :param s: входная строка
    :return: количество использованных символов, без учета повторений
    """
    list_chars: list = []
    for char in s:
        if char not in list_chars:
            list_chars.append(char)
    return len(list_chars)



def get_images_list_from_folder(folder: str, ext: str = "") -> []:
    prev_folder = os.getcwd()
    # print(f"get_images_list_from_folder: Исходная папка: {prev_folder}")
    if not os.path.isdir(folder):
        raise Exception(f"get_images_list_from_folder: Критическая ошибка. Папки с картинками {folder} нет.")
    os.chdir(folder)
    # print(f"get_images_list_from_folder: Текущая папка: {os.getcwd()}")
    # print(f"get_images_list_from_folder: Папка с изображениями: {folder}")
    dir_list = os.listdir()
    dir_list.sort()
    images = []  # pygame.image.load("img/01.png")
    for file_name in dir_list:
        if file_name.endswith(ext):
            # print(file_name)
            images.append(pygame.image.load(file_name))
    # print(len(images))
    # print(f"get_images_list_from_folder: Возврат в исходную папку: {os.getcwd()} => {prev_folder}")
    os.chdir(prev_folder)
    # print(f"Текущая папка: {os.getcwd()}")
    return images

