import os

import military_object
from globals import *
from input_line import InputLine
from list_menu import ListMenu


def screen_user_name() -> str:
    login = os.getlogin()  # системный логин
    login = login[0].upper() + login[1:]  # Первый символ перевести в Верхний Регистр
    username = login  # + '_{:%Y-%m-%d}'.format(datetime.now())
    print("OC: ", os.name)
    cwd = os.getcwd()
    print(f"путь: {cwd}")
    if not os.path.isdir(SAVE_DIR):
        print(f"Папки для сохранения результатов нет. Создаём: {SAVE_DIR}")
        os.mkdir(SAVE_DIR)
    os.chdir(SAVE_DIR)
    cwd = os.getcwd()
    # print(f"путь: {cwd}")
    dir_list = os.listdir(cwd)
    os.chdir("..")
    # print(os.getcwd())

    # print(f"--------\n"
    #       f"путь: {cwd}\n"
    #       f"{dir_list}\n"
    #       f"--------")
    # print(f"user prefix: {USER_FILE_PREFIX}")
    users: list = []
    for file_name in dir_list:
        if file_name[0:len(USER_FILE_PREFIX)] == USER_FILE_PREFIX:
            users.append(get_username_from_filename(filename=file_name))
    # print(f"--------\n"
    #       f"Игорьки:\n"
    #       f"{users}\n"
    #       f"--------")

    margin = 10
    r: pygame.Rect = pygame.Rect(MARGIN_W, MARGIN_H / 2, SCREEN_W - MARGIN_W * 2, 30)
    # print(f"рект для строки ввода: {r}")
    input_line = InputLine(
        rect=r.copy(),
        default_name=username
    )

    images = [
        pygame.image.load("img/name/hint_tab.png")
    ]
    img_rect = images[0].get_rect()
    img_rect.right = r.left - 5
    img_rect.top = r.top

    r.top = r.bottom + margin
    r.height = SCREEN_H // 4
    # print(f"рект для списка: {r}")
    list_menu = ListMenu(rect=r.copy(), items=users)

    while GamePhase.phase == Phases.USER_NAME:
        if time_to_draw_screen():
            SCREEN.fill(COLOR.BK)
            military_object.run_step()
            SCREEN.blit(images[0], img_rect)
            input_line.draw()
            list_menu.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if check_quit(event=event):
                    GamePhase.shift_prev()
                    break
                input_line.event_handler(event=event)
                list_menu.event_handler(event=event)
                if event.type == pygame.KEYDOWN:
                    # print(F"game_phase_intro_1. event:  {event}")
                    if event.key in [pygame.K_TAB, pygame.KSCAN_TAB]:
                        if input_line.status == STATUS.ACTIVE:
                            input_line.status = STATUS.PASSIVE
                            list_menu.status = STATUS.ACTIVE
                        else:
                            input_line.status = STATUS.ACTIVE
                            list_menu.status = STATUS.PASSIVE

                    if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        if input_line.status == STATUS.ACTIVE:
                            username = input_line.line_str  # !!!
                        else:
                            username = list_menu.line_str  # !!!

                        GamePhase.shift_next()
    return username
    # /while
