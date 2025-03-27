import datetime
from array import *

import pygame
from pygame.draw_py import Point
from pygame.event import EventType

from globals import *


class Control:

    def __init__(self):
        super().__init__()

        # статус органов управления
        self.key_shift: bool = False
        self.key_alt: bool = False
        self.key_ctrl: bool = False
        self.key_code: int = 0
        self.key_pres: bool = False
        self.key_repeat: bool = False
        self.key_pres_time: datetime.datetime = None
        self.key_repeat_time: datetime.datetime = None

        self.mouse_pos_x: int = 0
        self.mouse_pos_y: int = 0
        self.mouse_btn = array('b', [
            0,  # [0]
            0,  # [1] self.mouse_btn_1: bool = False  # 1 Левая
            0,  # [2] self.mouse_btn_2: bool = False  # 2 Колесо нажатие
            0,  # [3] self.mouse_btn_3: bool = False  # 3 Правая
            0,  # [4] self.mouse_btn_4: bool = False  # 4 Колесо вращение вперед
            0,  # [5] self.mouse_btn_5: bool = False  # 5 Колесо вращение назад
            0,  # [6] self.mouse_btn_6: bool = False  # 6 Вперед
            0]  # [7] self.mouse_btn_7: bool = False  # 7 Назад
                               )
        # pass

    def event_handler(self, event: EventType):
        if event.type == pygame.KEYDOWN:
            if event.key in KEYS_SHIFT:
                self.key_shift = True
            elif event.key in KEYS_ALT:
                self.key_alt = True
            elif event.key in KEYS_CTRL:
                self.key_ctrl = True
            else:
                self.key_code = event.key
                self.key_pres = True
                self.key_pres_time = datetime.now()
                print("KEY DOWN: ", event.key)

        elif event.type == pygame.KEYUP:
            if event.key in KEYS_SHIFT:
                self.key_shift = False
            elif event.key in KEYS_ALT:
                self.key_alt = False
            elif event.key in KEYS_CTRL:
                self.key_ctrl = False
            else:
                self.key_code = event.key
                self.key_pres = False
                self.key_pres_time = datetime.now()
                print(f"KEY UP: {event.key}, {datetime.now() - self.key_pres_time} ms")

        if self.key_pres:
            if (datetime.now() - self.key_pres_time) > AUTO_REPEAT_WAIT:
                self.key_repeat = True
                self.key_repeat_time = datetime.now()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_pos_x, self.mouse_pos_y = event.pos
            self.mouse_btn[event.button] = 1
            # print("CTRL MOUSE BTN DN: ", event.pos, event.button)
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_pos_x, self.mouse_pos_y = event.pos
            self.mouse_btn[event.button] = 0
            # print("CTRL MOUSE BTN UP: ", event.pos, event.button)
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos_x, self.mouse_pos_y = event.pos
            # print("CTRL MOUSE MOV: ", event.pos)
