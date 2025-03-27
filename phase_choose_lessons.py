import globals
import military_object
from chars import mark_char_line
from globals import *
import random
from screen_keyboard import keyboard
from phase_init import get_words_by_chars, get_lesson
from t_menu import TMenu
from t_table import TTable


def choose_lessons(username: str) -> list:
    font_size: int = 22
    font_interline = 4
    font = pygame.font.Font(None, font_size)
    menu_rect = LINE_RECT

    user_conf: list = read_user_data(username=username)
    if user_conf is None:
        user_conf = read_conf(CONF_LESSONS)

    globals.SEVERITY_ERRORS = user_conf["SEVERITY_ERRORS"]
    lesson_generate_symbols: int = round(float(user_conf["time_one_lesson"] / 60) * user_conf["speed_cpm"])
    # print(f"Символов в уроке: [{lesson_generate_symbols}]")
    # print("Уроки:")
    # print(lessons)
    for lesson in user_conf["lessons"]:
        if "do_training" not in lesson:
            lesson["do_training"] = True
        if "ok_training" not in lesson:
            lesson["ok_training"] = 0
        if "rating" not in lesson:
            lesson["rating"] = 0.0
        if "speed" not in lesson:
            lesson["speed"] = 0.0
        if ("str" not in lesson) | (user_conf["REGENERATE_STR"]):
            # print(f"lesson: {lesson}")
            match lesson["lesson_src"]:
                case "chars":
                    lesson["str"] = ""
                    for i in range(lesson_generate_symbols):
                        lesson["str"] = lesson["str"] + random.choice(lesson["generate_str"])

                case "words":
                    word_set = get_words_by_chars(stage_list=None, stage_dict=globals.ALL_WORDS, included_chars=lesson["generate_str"])
                    lesson["str"] = get_lesson(word_set=word_set, count_chars=lesson_generate_symbols)

                case "fixed":
                    if len(lesson["fixed_str"]) > 0:
                        lesson["str"] = lesson["fixed_str"]
                    else:
                        raise Exception('Ошибка в структуре генерации урока: "lesson_src" указан в "fixed", но "fixed_str" пустая строка:\n[{}]'.format(lesson))

                case _:
                    raise Exception('Ошибка в структуре генерации урока: Не известный источник символов для урока "lesson_src": {}'.format(lesson["lesson_src"]))

    lessons_count = len(user_conf["lessons"])

    table_rec = [
        [
            {"text": "[стрелки|PdUp|PgDown|Home|End]  Перемещение", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": "[пробел]  Включение/выключение урока", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": "[+|-]  Включить/Выключить все уроки", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT}
        ],
        [
            {"text": "[Имя] [Скорость] [Рейтинг] [Прохождений]", "h_align": ALIGN.CENTER, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.BLACK80},
            {"text": "[Esc]  Вернуться назад", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT},
            {"text": "[Enter]  Начать тренировку", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT}
        ]
    ]

    table: TTable = TTable(table_rec=table_rec, font=get_font_default(font_size=16))
    table.rect.center = LINE_RECT.center
    table.rect.top = LINE_RECT.bottom + 8

    # print(f"Количество уроков: {lessons_count}")
    title = ["Выберите уроки"]
    menu: TMenu = TMenu(rect=LINE_RECT, conf=user_conf)
    while GamePhase.phase == Phases.CHOOSE_LESSONS:
        if time_to_draw_screen():
            SCREEN.fill(COLOR.BK)
            military_object.run_step()
            # pygame.draw.rect(SCREEN, COLOR.BLACK40, WORK_RECT, 1)
            draw_paragraph(paragraph=title, color=COLOR.GREEN,
                           rect=RectType(menu_rect.x, 0, menu_rect.width, menu_rect.y))
            keyboard.draw(Phases.CHOOSE_LESSONS)
            menu.update()
            menu.draw()
            table.draw()
            keyboard.draw(Phases.POST)
            pygame.display.flip()

            for event in pygame.event.get():
                if check_quit(event):
                    GamePhase.shift_prev()
                    break
                menu.event_handler(event=event)
                if menu.status == STATUS.END:
                    save_user_data(username=username, conf=user_conf)
                    GamePhase.shift_next()
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # mouse_pos_x, mouse_pos_y = event.pos
                    print("MOUSE BTN DN: ", event.pos)

    # print("Состояние уроков:")
    # print(LESSONS)
    # print("----")
    return user_conf
