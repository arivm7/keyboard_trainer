import datetime
import json
import os
import random
import warnings
from pygame.event import EventType
import pygame
from chars import mark_char_line
from digit_fly import DigitFly
from globals import *
from input_line import InputLine
from list_menu import ListMenu
from military_object import MilitaryObject, ACTORS, AttackTo
from mo_01_flyer import Fly01
from mo_02_sova import Fly02_Sova
from mo_02_vetka import Fly02_Vetka
from mo_03_marik import Mo03_Marik
from phase_end import game_phase_end
from phase_intro_0 import *
from phase_intro_1 import *
from phase_intro_2 import *
from phase_run import game_phase_run
from phase_user_name import *
from phase_choose_lessons import *
from phase_result import *
from screen_keyboard import ScreenKeyboard
from line_chars import LineChars
from my_stats import MyStats


warnings.filterwarnings("ignore", category=DeprecationWarning)


def run():
    # for ch in S1:
    #     print(eval(f"pygame.K_{ch}"), ord(ch))

    # print("AUTO_REPEAT_WAIT: ", AUTO_REPEAT_WAIT)
    # print("AUTO_REPEAT_ON:: ", AUTO_REPEAT_ON)

    # event: EventType
    username: str | None = None
    lessons: list | None = None

    fly01 = Fly01()
    ACTORS.append(fly01)
    vetka = Fly02_Vetka()
    vetka.aliens.append(fly01)
    ACTORS.append(vetka)
    sova = Fly02_Sova()
    ACTORS.append(sova)
    marik1 = Mo03_Marik()
    marik1.aliens.append(fly01)
    ACTORS.append(marik1)
    marik2 = Mo03_Marik()
    marik2.aliens.append(fly01)
    ACTORS.append(marik2)
    # bullet = Bullet(start_from=Point(300, 300), attack_to=AttackTo(None, None, None, fly01))
    # ACTORS.append(bullet)
    sova.parkings.append(vetka)
    print(f"Объектов: {len(ACTORS)}")

    GamePhase.phase = GamePhase.INTRO_0

    while GamePhase.phase != Phases.QUIT:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         print("MAIN. RUN. BTN: ", event.pos, event.button)
        #     # if event.type == pygame.MOUSEMOTION:
        #     #     print("MOV: ", event.pos)
        match GamePhase.phase:
            case Phases.INTRO_0:
                game_phase_intro_0()  # Сцена рассказывающая о результатах тренировок
            case Phases.USER_NAME:
                username = screen_user_name()  # Сцена выбора имени игрока и загрузка сохраненной игры, если есть.
            case Phases.CHOOSE_LESSONS:
                lessons = choose_lessons(username=username)  # Сцена выбора уроков для тренировки
            case Phases.INTRO_1:
                game_phase_intro_1()  # Сцена "Расположите пальцы на кнопках"
            case Phases.INTRO_2:
                game_phase_intro_2()  # Сцена "Приготовьтесь, нажмите любую кнопку для начала игры"
            case Phases.GAME_RUN:
                game_phase_run(username=username, conf=lessons)
            case Phases.GAME_RESULT:
                game_phase_result(username=username, conf=lessons)
            case Phases.GAME_END:
                game_phase_end()
            case Phases.GAME_NONE:
                break
            case _:
                print_color(F"MAIN. не обрабатываемая фаза игры {GamePhase.phase} ", console_color=COLOR.RED)
                GamePhase.phase = Phases.QUIT
                exit(10)

    print("Нормальное завершение")
# ----------------


run()
