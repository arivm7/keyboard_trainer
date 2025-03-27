import military_object
from digit_fly import DigitFly
from globals import *
from line_chars import LineChars
from screen_keyboard import keyboard
from my_stats import MyStats


def game_pre_run_counter(rect: RectType = None) -> bool:
    """
    Счетчик перед началом урока. Можно подождать, нажать любую кнопку или нажать ESC для возврата False
    :param rect: область отрисовки счетчика. Остальной экран не трогается
    :return: true -- если нормальное завершение, false -- если нажата кнопка отмены
    """
    if rect is None:
        rect = RectType(LINE_RECT.x + 5, LINE_RECT.y + 5, LINE_RECT.w - 10, LINE_RECT.h - 10)
    pre_run_countdown = [
        DigitFly(hint="5"),
        DigitFly(hint="4"),
        DigitFly(hint="3"),
        DigitFly(hint="2"),
        DigitFly(hint="1")
    ]
    pre_run_index = 0
    result: bool = True
    do_running: bool = True
    while do_running:
        if time_to_draw_screen():
            pygame.draw.rect(surface=SCREEN, color=COLOR.BK, rect=rect)
            # pygame.draw.rect(surface=SCREEN, color=COLOR.BLACK20, rect=rect, width=1)
            # pygame.draw.rect(surface=SCREEN, color=COLOR.BLACK20, rect=LINE_RECT, width=1)
            # SCREEN.fill(COLOR.BK)
            if pre_run_countdown[pre_run_index].status == STATUS.ACTIVE:
                pre_run_countdown[pre_run_index].update()
                pre_run_countdown[pre_run_index].draw()
            else:
                pre_run_index += 1
                if pre_run_index >= len(pre_run_countdown):
                    do_running = False
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    do_running = False
                    if check_quit(event=event):
                        result = False
    pygame.draw.rect(surface=SCREEN, color=COLOR.BK, rect=rect)
    return result


# ----------------

font_list_lessons = pygame.font.Font(None, 20)
selector_img: pygame.Surface = font_list_lessons.render("->", ANTIALIASING, COLOR.MENU)
selector_img_rect = selector_img.get_rect()


def draw_list_lessons_for_game(lessons: list, current_lesson: list, rect: RectType):
    global selector_img
    px: int = rect.left
    py: int = rect.top
    dy = 18  # selector_img.get_rect().height
    lessons_count = len(lessons["lessons"])
    count_on_rect: int = rect.height // dy
    if lessons_count > count_on_rect:
        # поиск index текущего урока
        current_index: int = 0
        for index in range(0, lessons_count, 1):
            if current_lesson["name"] == lessons["lessons"][index]["name"]:
                current_index = index
                break
        # Вычисление index_top & index_bottom
        index_top: int = current_index - (count_on_rect // 2)
        if index_top < 0:
            index_top = 0
        index_bottom = index_top + count_on_rect - 1
        if index_bottom > (lessons_count - 1):
            index_bottom = lessons_count - 1
            index_top = index_bottom - count_on_rect + 1
    else:
        index_top = 0
        index_bottom = lessons_count - 1

    if index_top > 0:
        pygame.draw.polygon(surface=SCREEN,
                            color=COLOR.GREEN,
                            points=[(rect.x + CHAR_WIDTH * 1.5, rect.y),
                                    (rect.x + CHAR_WIDTH * 2, rect.y + 7),
                                    (rect.x + CHAR_WIDTH, rect.y + 7)])

    if index_bottom < (lessons_count - 1):
        pygame.draw.polygon(surface=SCREEN,
                            color=COLOR.GREEN,
                            points=[(rect.right - CHAR_WIDTH * 1.5, rect.bottom),
                                    (rect.right - CHAR_WIDTH * 2, rect.bottom - 7),
                                    (rect.right - CHAR_WIDTH, rect.bottom - 7)])

    for index in range(index_top, index_bottom + 1, 1):
        if current_lesson["name"] == lessons["lessons"][index]["name"]:
            r: RectType = rect.copy()
            r.topleft = px, py
            SCREEN.blit(selector_img, r)
        r: RectType = lessons["lessons"][index]["img_name"].get_rect()
        r.topleft = px + 20, py
        # print("l: ", l["name"], "R: ", r, " rect: ", rect)
        SCREEN.blit(lessons["lessons"][index]["img_name"], r)
        r2: RectType = lessons["lessons"][index]["img_rating"].get_rect()
        r2.top = r.top
        r2.right = rect.right - 5
        SCREEN.blit(lessons["lessons"][index]["img_rating"], r2)
        py += dy


def game_phase_run(username: str, conf: list):
    # print(f"lessons: {lessons}")

    global font_list_lessons
    rect_list_lessons = RectType(0, LINE_RECT.y, LINE_RECT.x, LINE_RECT.height)
    current_lesson_index: int = 0
    for lesson in conf["lessons"]:
        lesson["img_name"]: pygame.Surface = font_list_lessons.render(lesson["name"], ANTIALIASING, COLOR.MENU)
        # print(lesson["name"], lesson["img_name"])

    for lesson in conf["lessons"]:
        # print(f"lesson: {lesson}")
        if not lesson["do_training"]:
            continue
        for l in conf["lessons"]:
            l["img_rating"]: pygame.Surface = font_list_lessons.render(str(int(l["rating"])), ANTIALIASING, COLOR.MENU_RATING)
        # preRunCounter = True  # GamePhase.phase = Phases.GAME_PRE_RUN
        line = LineChars(line_str=lesson["str"], is_words=(lesson["lesson_src"] == "words"))
        stats = MyStats(line)
        # счетчик перед началом игры
        if game_pre_run_counter():
            # print("Урок")
            # --------------------------
            while GamePhase.phase in [Phases.GAME_RUN]:  # Phases.GAME_PRE_RUN
                if time_to_draw_screen():
                    line.update()
                    stats.update()
                    keyboard.update()

                    if line.status == STATUS.END:
                        lesson['ok_training'] = int(lesson['ok_training']) + 1
                        if stats.draw_final(rect=LINE_RECT):
                            lesson['rating'] = stats.rating
                            lesson['speed'] = stats.speed
                            break
                        else:
                            line.re_init()

                    # DRAW START
                    SCREEN.fill(COLOR.BK)
                    military_object.run_step()
                    keyboard.draw(Phases.PRE)

                    # отрисовка списка уроков
                    draw_list_lessons_for_game(lessons=conf, current_lesson=lesson, rect=rect_list_lessons)

                    line.draw()
                    stats.draw()
                    keyboard.draw(Phases.POST)
                    pygame.display.flip()
                    # DRAW END

                    for event in pygame.event.get():
                        if check_quit(event=event):
                            GamePhase.shift_prev()
                            break
                        line.event_handler(event=event)

        else:
            # Если нажата кнопка "отмены", то
            # выход из цикла перебора уроков игры
            # for lesson in lessons["lessons"]:
            print("отмена урока")
            GamePhase.shift_prev()
            GamePhase.shift_prev()
            break

        if line.status == STATUS.END:
            # нормальное завершение игрового урока
            # все показали и проверили в цикле урока

            # lesson['ok_training'] = int(lesson['ok_training']) + 1
            # if stats.draw_final(rect=LINE_RECT):
            #     lesson['rating'] = stats.rating
            #     lesson['speed'] = stats.speed
            # else:
            #     line.re_init()

            # разве что сохранить...
            pass

        # print(f"line.status ({line.status}) == STATUS.END ({STATUS.END})")
        #  запись статистики урока в lesson
        #  line, stats --> lessons
        pass

    print("Конец игры")
    save_user_data(username=username, conf=conf)
    #  ALL LESSONS STATUS
    GamePhase.shift_next()





