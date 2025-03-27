from globals import *
from line_chars import LineChars
from t_table import TTable


class MyStats:
    MARGIN = 5

    def __init__(self, line_chars: LineChars):
        self.screen: pygame.Surface = SCREEN
        self.line: LineChars = line_chars
        self.count_chars: int = len(self.line.line)

        self.count_success: int = 0
        self.time_success: float = 0.0  # seconds
        self.speed_success: float = 0.0

        self.count_failed: int = 0
        self.time_failed: float = 0.0  # seconds
        self.speed_failed: float = 0.0

        self.count: int = 0
        self.speed: float = 0.0
        self.rating: float = 0.0

        self.rect: pygame.Rect = pygame.Rect(SCREEN_W - MARGIN_W + self.MARGIN, MARGIN_H, MARGIN_W, WORK_RECT.height)
        self.font: pygame.font.Font = pygame.font.Font(None, 20)
        self.label_total_chars = self.font.render(str("Строка:"), ANTIALIASING, COLOR.BLACK20)
        self.label_total_chars_val = self.font.render(str(self.count_chars), ANTIALIASING, COLOR.BLACK20)
        self.label_total_green = self.font.render(str("Попадания:"), ANTIALIASING, COLOR.GREEN)
        self.label_total_failed = self.font.render(str("Промахи:"), ANTIALIASING, COLOR.RED)
        self.label_total_width: int = max(
            self.label_total_chars.get_rect().width,
            self.label_total_green.get_rect().width,
            self.label_total_failed.get_rect().width
        )

    def update(self):
        self.count_success = 0
        self.time_success = 0.0
        self.count_failed = 0
        self.time_failed = 0.0
        for char in self.line.line:
            if char.status == STATUS.QUEUE:
                continue
            elif char.status == STATUS.ACTIVE:
                continue
            elif char.status == STATUS.SUCCESS:
                self.count_success += 1
                self.time_success += char.green_delta.total_seconds()
                self.speed_success = (self.count_success / self.time_success) * 60
            elif char.status == STATUS.FAILED:
                self.count_failed += 1
                self.time_failed += char.failed_delta.total_seconds()
                self.speed_failed = (self.count_failed / self.time_failed) * 60
        self.count = self.count_success + self.count_failed
        if (self.count_success + self.count_failed) > 0:
            self.speed = self.speed_success * (self.count_success / self.count) - \
                         self.speed_failed * (self.count_failed / self.count) * SEVERITY_ERRORS
        else:
            self.speed = 0
        self.rating = self.speed * (self.line.line_count_chars / MAX_LESSON_LEN)
        self.line.rating = self.rating

    def draw(self):
        px1 = self.rect.left
        px2 = px1 + self.label_total_width + self.MARGIN

        # 1 строка
        # всего символов в уроке
        py = self.rect.top
        r = self.label_total_chars.get_rect()
        r.topright = (px1 + self.label_total_width, py)
        self.screen.blit(self.label_total_chars, r)

        r = self.label_total_chars_val.get_rect()
        r.topleft = (px2, py)
        self.screen.blit(self.label_total_chars_val, r)

        # 2 строка
        # всего правильных нажатий (% от общего)
        py += r.height + self.MARGIN
        r = self.label_total_green.get_rect()
        r.topright = (px1 + self.label_total_width, py)
        self.screen.blit(self.label_total_green, r)

        if self.count_success > 0:
            img = self.font.render(str(f"{self.count_success:5.0f}" + " [" + str(
                int(100 * self.count_success / (self.count_success + self.count_failed))) + "%]"), ANTIALIASING,
                                   COLOR.GREEN)
        else:
            img = self.font.render(str(f"{self.count_success:5.0f}"), ANTIALIASING, COLOR.GREEN)
        r = img.get_rect()
        r.topleft = (px2, py)
        self.screen.blit(img, r)

        # 3 строка
        # количество промахов (%)
        py += r.height + self.MARGIN
        r = self.label_total_failed.get_rect()
        r.topright = (px1 + self.label_total_width, py)
        self.screen.blit(self.label_total_failed, r)

        if self.count_failed > 0:
            img = self.font.render(str(f"{self.count_failed:5.0f}" + " [" + str(
                int(100 * self.count_failed / (self.count_failed + self.count_success))) + "%]"), ANTIALIASING,
                                   COLOR.RED)
        else:
            img = self.font.render(f"{self.count_failed:5.0f}", ANTIALIASING, COLOR.RED)
        r = img.get_rect()
        r.topleft = (px2, py)
        self.screen.blit(img, r)

        # 4 строка
        # время
        py += r.height + self.MARGIN
        time_float = (datetime.now() - self.line.time_start).total_seconds()
        time_str = f"{time_float:9.0f} c :"
        img = self.font.render(time_str, ANTIALIASING, COLOR.RED)
        r = img.get_rect()
        r.topright = (px1 + self.label_total_width, py)
        self.screen.blit(img, r)

        # скорость правильного набора (%)
        img = self.font.render(str(f"{self.speed_success:5.0f} зн/мин"), ANTIALIASING, COLOR.GREEN)
        r = img.get_rect()
        r.topleft = (px2, py)
        self.screen.blit(img, r)

        # скорость ошибочного набора (%)
        py += r.height + self.MARGIN
        img = self.font.render(str(f"{self.speed_failed:5.0f} зн/мин"), ANTIALIASING, COLOR.FAIL)
        r = img.get_rect()
        r.topleft = (px2, py)
        self.screen.blit(img, r)

        # скорость общая
        py += r.height + self.MARGIN
        img = self.font.render(str(f"{self.speed:5.0f} зн/мин"), ANTIALIASING, COLOR.GREEN)
        r = img.get_rect()
        r.topleft = (px2, py)
        self.screen.blit(img, r)

        # рейтинг
        py += r.height + self.MARGIN
        img = self.font.render(str(f"{self.rating:5.0f} рейтинг"), ANTIALIASING, COLOR.GREEN)
        r = img.get_rect()
        r.topleft = (px2, py)
        self.screen.blit(img, r)

    def draw_final(self, rect: RectType) -> bool:

        #  text_str:
        #     "text": "",
        #     "padding": 1,
        #     "h_align": ALIGN.RIGHT,
        #     "v_align": ALIGN.CENTER,
        #     "text_color": COLOR.TEXT_DEFAULT,
        #     "bk_color": COLOR.BK,
        #     "font": FONT_DEFAULT,
        #     "frame_width": 1,
        #     "frame_color": COLOR.TEXT_DEFAULT

        table_rec = [
            [
                {'text': "Время выполнения урока"},
                {'text': f"{((datetime.now() - self.line.time_start).total_seconds()):5.0f}", 'h_align': ALIGN.RIGHT},
                {'text': "сек"}
            ],
            [
                {"text": "Всего символов в уроке"},
                {"text": f"{self.count_chars:5.0f}", "h_align": ALIGN.RIGHT},
                {"text": "зн."}
            ],
            [
                {"text": "Всего правильных нажатий"},
                {"text": f"{self.count_success:5.0f}", "h_align": ALIGN.RIGHT, 'text_color': COLOR.GREEN},
                {"text": str(int(100 * self.count_success / (self.count_success + self.count_failed))) + "%", 'text_color': COLOR.GREEN}
            ],
            [
                {"text": "Количество промахов"},
                {"text": f"{self.count_failed:5.0f}", "h_align": ALIGN.RIGHT, 'text_color': COLOR.FAIL},
                {"text": str(int(100 * self.count_failed / (self.count_failed + self.count_success))) + "%", 'text_color': COLOR.FAIL}
            ],
            [
                {"text": "Скорость правильного набора"},
                {"text": f"{self.speed_success:5.0f}", "h_align": ALIGN.RIGHT, 'text_color': COLOR.GREEN},
                {"text": "зн/мин", 'text_color': COLOR.GREEN}
            ],
            [
                {"text": "Скорость ошибочного набора"},
                {"text": f"{self.speed_failed:5.0f}", "h_align": ALIGN.RIGHT, 'text_color': COLOR.FAIL},
                {"text": "зн/мин", 'text_color': COLOR.FAIL}
            ],
            [
                {"text": "Скорость общая", 'text_color': COLOR.YELLOW, "bk_color": COLOR.MENU_BK_SELECTED},
                {"text": f"{self.speed:5.0f}", "h_align": ALIGN.RIGHT, 'text_color': COLOR.YELLOW, "bk_color": COLOR.MENU_BK_SELECTED},
                {"text": "зн/мин", 'text_color': COLOR.YELLOW, "bk_color": COLOR.MENU_BK_SELECTED}
            ],
            [
                {"text": "Рейтинг", 'text_color': COLOR.YELLOW, "bk_color": COLOR.MENU_BK_SELECTED},
                {"text": f"{self.rating:5.0f}", "h_align": ALIGN.RIGHT, 'text_color': COLOR.YELLOW, "bk_color": COLOR.MENU_BK_SELECTED},
                {"text": "", 'text_color': COLOR.YELLOW, "bk_color": COLOR.MENU_BK_SELECTED}
            ]
        ]

        table_result: TTable = TTable(table_rec=table_rec, font=get_font_default(font_size=32))
        table_result.rect.center = LINE_RECT.center

        table_hint = [
            [
                {"text": "[Esc]  Пройти урок еще раз", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT}
            ],
            [
                {"text": "[Enter]  Подтвердить и перейти к следующему уроку", "h_align": ALIGN.LEFT, "bk_color": COLOR.MENU_BK_SELECTED, 'text_color': COLOR.TEXT_DEFAULT}
            ]
        ]

        table2: TTable = TTable(table_rec=table_hint, font=get_font_default(font_size=16))
        table2.rect.center = LINE_RECT.center
        table2.rect.top = LINE_RECT.bottom + 8

        result: bool = True
        do_running: bool = True
        while do_running:
            if time_to_draw_screen():
                pygame.draw.rect(surface=SCREEN, color=COLOR.BK, rect=table_result.rect)
                table_result.draw()
                table2.draw()
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if check_quit(event=event):
                            result = False
                            do_running = False
                        if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                            do_running = False
        pygame.draw.rect(surface=SCREEN, color=COLOR.BK, rect=rect)
        return result
