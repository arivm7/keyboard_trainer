import military_object
from globals import *
from screen_keyboard import keyboard
from show_images import ShowImages
from t_table import TTable


def game_phase_result(username: str, conf: list):
    count_lessons: int = len(conf["lessons"])  # всего уроков
    count_success: int = 0  # пройденных уроков
    count_no_trained: int = 0  # не пройденных уроков
    max_chars_per_lesson: int = 0
    max_rating: float = 0.0
    max_speed: float = 0.0
    max_relative_rating: float | None = None
    max_relative_speed: float | None = None

    for lesson in conf["lessons"]:
        c = count_chars(lesson["str"])
        if max_chars_per_lesson < c:
            max_chars_per_lesson = c
        if max_rating < lesson["rating"]:
            max_rating = lesson["rating"]
        if max_speed < lesson["speed"]:
            max_speed = lesson["speed"]
        if lesson["ok_training"] > 0:
            count_success += 1
        else:
            count_no_trained += 1

    for lesson in conf["lessons"]:
        c = count_chars(lesson["str"])
        lesson["relative_rating"] = lesson["rating"] * (c / max_chars_per_lesson)
        lesson["relative_speed"] = lesson["speed"] * (c / max_chars_per_lesson)

        if max_relative_rating is not None:
            max_relative_rating += lesson["relative_rating"]
        else:
            max_relative_rating = lesson["relative_rating"]

        if max_relative_speed is not None:
            if max_relative_speed < lesson["relative_speed"]:
                max_relative_speed = lesson["relative_speed"]
        else:
            max_relative_speed = lesson["relative_speed"]

        if count_no_trained == 0:
            hint: list[str] = ["Поздравляем! Вы прошли все уроки!"]
        elif (max(count_success, count_no_trained) / min(count_success, count_no_trained)) <= 1.5:
            hint: list[str] = ["Поздравляем! Вы на половине пути к успеху!"]
        elif count_success > count_no_trained:
            hint: list[str] = ["Поздравляем! Вы прошли большую часть уроков!"]
        else:
            hint: list[str] = ["Вы прошли выбранные уроки, но это только начало!"]

    video: ShowImages = ShowImages(folder="img/final/01", repeat=True, px=LINE_RECT.centerx, py=LINE_RECT.centery)

    table_rec = [
        [
            {"text": "Всего уроков в курсе:", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": str(count_lessons), "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": "", "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT}
        ],
        [
            {"text": "Пройдено уроков:", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": str(count_success), "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": "", "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT}
        ],
        [
            {"text": "Пропущено уроков:", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": str(count_no_trained), "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": "", "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT}
        ],
        [
            {"text": "Наибольший рейтинг:", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": str(round(max_rating)), "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": "", "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT}
        ],
        [
            {"text": "Относительный рейтинг по всем урокам:", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": str(round(max_relative_rating)), "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.YELLOW},
            {"text": "", "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT}
        ],
        [
            {"text": "Наибольшая скорость:", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": str(round(max_speed)), "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": "зн/мин", "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT}
        ],
        [
            {"text": "Относительная скорость по всем урокам:", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": str(round(max_relative_speed)), "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.YELLOW},
            {"text": "зн/мин", "h_align": ALIGN.RIGHT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT}
        ],
    ]

    table: TTable = TTable(table_rec=table_rec, font=get_font_default(font_size=26))
    table.rect.centerx = LINE_RECT.centerx
    table.rect.centery = LINE_RECT.bottom + ((SCREEN_H - LINE_RECT.bottom) // 2)

    while GamePhase.phase == Phases.GAME_RESULT:
        if time_to_draw_screen():

            SCREEN.fill(COLOR.BK)
            military_object.run_step()
            keyboard.draw(Phases.GAME_RESULT)
            draw_paragraph(paragraph=hint, color=COLOR.YELLOW, rect=RectType(LINE_RECT.x, 0, LINE_RECT.width, LINE_RECT.y))
            video.update()
            video.draw()
            table.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                video.event_handler(event=event)
                if check_quit(event):
                    GamePhase.shift_prev()
                    break
                if event.type == pygame.KEYDOWN:
                    # print(F"game_phase_intro_1. event:  {event}")
                    # print(F"game_phase_intro_1. GAME_PHASE: {GAME_PHASE} -> {PHASE.GAME_PRE_RUN}")
                    if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        GamePhase.shift_next()
