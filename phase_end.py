import random

import pygame

import military_object
from globals import *
from image_fly import ImageFly
from screen_keyboard import keyboard
from show_images import ShowImages
from t_table import TTable


def game_phase_end():

    folder: str = "img/end"

    # print("game_phase_end: Считывание картинок")
    prev_folder = os.getcwd()
    # print(f"game_phase_end: Исходная папка: {prev_folder}")
    # print(f"game_phase_end: Папка с изображениями: {folder}")
    if not os.path.isdir(folder):
        raise Exception("show_images: init: Критическая ошибка. Папки с картинками нет.")
    os.chdir(folder)
    # print(f"game_phase_end: Папка с изображениями: {os.getcwd()}")
    dir_list = os.listdir()
    dir_list.sort()
    # print(f"game_phase_end: dir_list: {dir_list}")
    file_name: str = random.choice(dir_list)
    # print(f"game_phase_end: file_name: {file_name}")
    image: pygame.Surface = pygame.image.load(file_name)
    os.chdir(prev_folder)
    # print(f"show_images: Вернулись в исходную папку: {os.getcwd()}")

    img_fly: ImageFly = ImageFly(image=image)

    while GamePhase.phase == Phases.GAME_END:
        if time_to_draw_screen():

            SCREEN.fill(COLOR.BK)
            military_object.run_step()
            keyboard.draw(Phases.GAME_RESULT)
            img_fly.update()
            img_fly.draw()
            pygame.display.flip()

            if img_fly.status == STATUS.NONE:
                GamePhase.phase = GamePhase.QUIT
                break

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # print(F"game_phase_intro_1. event:  {event}")
                    # print(F"game_phase_intro_1. GAME_PHASE: {GAME_PHASE} -> {PHASE.GAME_PRE_RUN}")
                    GamePhase.phase = GamePhase.QUIT
                    break
