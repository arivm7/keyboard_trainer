from globals import *
import pygame
from pygame.event import EventType
from datetime import *


class OneChar:
    def __init__(self,
                 char_str: str,
                 key_code: int,
                 key_shift: bool = False,
                 key_alt: bool = False,
                 key_ctrl: bool = False,
                 kb_layout: int = KB_LAYOUT_EN,
                 kb_px: int = None,
                 kb_py: int = None):
        self.screen: pygame.Surface = SCREEN
        # Ожидаемое состояние клавиатуры
        self.char_str: str = char_str
        self.char_code: int = key_code
        self.char_shift: bool = key_shift
        self.char_alt: bool = key_alt
        self.char_ctrl: bool = key_ctrl
        self.char_layout: int = kb_layout
        self.kb_px: int = kb_px
        self.kb_py: int = kb_py
        # статус кнопок клавиатуры
        self.key_shift_pressed: bool = False
        self.key_alt_pressed: bool = False
        self.key_ctrl_pressed: bool = False
        self.key_code_pressed: int = 0
        # self.key_repeat: bool = False
        self.key_pres_time: datetime | None = None
        self.key_repeat_time: datetime | None = None

        if self.char_str != " ":
            self.font = FONT_DEFAULT
            self.image_queue = self.font.render(str(self.char_str), ANTIALIASING, COLOR.QUEUE)
            self.image_active = self.font.render(str(self.char_str), ANTIALIASING, COLOR.CURRENT)
            self.image_red = self.font.render(str(self.char_str), ANTIALIASING, COLOR.RED)
            self.image_green = self.font.render(str(self.char_str), ANTIALIASING, COLOR.GREEN)
            self.image_fail = self.font.render(str(self.char_str), ANTIALIASING, COLOR.FAIL)
            self.rect: pygame.Rect = self.image_queue.get_rect()
        else:
            self.rect: pygame.Rect = pygame.Rect(0, 0, CHAR_WIDTH / 2, 1)
        self.width = self.rect.width
        self._status: int = STATUS.QUEUE
        self._active_start: datetime | None = None
        self._active_end: datetime | None = None
        self._green_delta: timedelta | None = None
        self._failed_delta: timedelta | None = None
        self.post_signal_count: int = 15
        self.post_signal_rect: RectType = RectType(0, 0, 40, 30)

    def re_init(self):
        self._status = STATUS.QUEUE
        self.key_code_pressed: int = 0
        self.key_pres_time = None
        self.key_repeat_time = None
        self._active_start = None
        self._active_end = None
        self._green_delta = None
        self._failed_delta = None

    def update(self):
        if self.status == STATUS.ACTIVE:
            if self.key_code_pressed > 0:
                if self.im_pressed():
                    self.status = STATUS.SUCCESS
                    # print(f"Char: UPDATE GREEN: {self.char_str} -> [{self.status}]")
                else:
                    self.status = STATUS.FAILED
                    # print(f"Char: UPDATE FAILED: {self.char_str} -> [{self.status}]")

    def draw_post_signal(self):
        if self.post_signal_count > 0:
            self.post_signal_rect.center = self.kb_px, self.kb_py
            if self.status == STATUS.FAILED:
                pygame.draw.ellipse(surface=self.screen, color=COLOR.RED, rect=self.post_signal_rect, width=3)
            elif self.status == STATUS.SUCCESS:
                pygame.draw.ellipse(surface=self.screen, color=COLOR.GREEN, rect=self.post_signal_rect, width=3)
            self.post_signal_rect.inflate_ip(1, 1)
            self.post_signal_count -= 1

    def draw_helper(self):
        # pygame.draw.circle(surface=self.screen, color=COLOR.HELP, center=(self.kb_px, self.kb_py), radius=20, width=0)
        r = pygame.Rect(0, 0, 40, 30)
        r.center = self.kb_px, self.kb_py
        pygame.draw.ellipse(surface=self.screen, color=COLOR.HELP_KEY, rect=r, width=0)

    def draw(self, px: float, py: float):
        if self.char_str == " ":
            self.rect.midleft = (px, py + CHAR_HEIGHT / 3)
        else:
            self.rect.midleft = (px, py)
        if self.status == STATUS.QUEUE:
            if self.char_str == " ":
                pygame.draw.rect(surface=self.screen, color=COLOR.QUEUE, rect=self.rect, width=0)
            else:
                # pygame.draw.rect(surface=self.screen, color=COLOR.QUEUE, rect=self.rect, width=1)
                self.screen.blit(self.image_queue, self.rect)

        elif self.status == STATUS.ACTIVE:
            if self.char_str == " ":
                pygame.draw.rect(surface=self.screen, color=COLOR.CURRENT, rect=self.rect, width=0)
            else:
                # pygame.draw.rect(surface=self.screen, color=COLOR.CURRENT, rect=self.rect, width=1)
                self.screen.blit(self.image_active, self.rect)
            pygame.draw.rect(
                surface=self.screen, color=COLOR.UNDERLINE,
                rect=(px + self.rect.width / 2 - CHAR_WIDTH / 2, py + CHAR_HEIGHT / 2.5, CHAR_WIDTH, 4),
                width=0)
            self.draw_helper()

        elif self.status == STATUS.FAILED:
            if self.char_str == " ":
                pygame.draw.rect(surface=self.screen, color=COLOR.FAIL, rect=self.rect, width=0)
            else:
                # pygame.draw.rect(surface=self.screen, color=COLOR.FAIL, rect=self.rect, width=1)
                self.screen.blit(self.image_fail, self.rect)
            self.draw_post_signal()

        elif self.status == STATUS.SUCCESS:
            if self.char_str == " ":
                pygame.draw.rect(surface=self.screen, color=COLOR.SUCCESS, rect=self.rect, width=0)
            else:
                # pygame.draw.rect(surface=self.screen, color=COLOR.GREEN, rect=self.rect, width=1)
                self.screen.blit(self.image_green, self.rect)
            self.draw_post_signal()

        else:
            print(f"Критическая ошибка: Char.DRAW: [{self.status}] -- необработанный статус символа")
            exit(10)

    def im_pressed(self):
        return (self.char_code == self.key_code_pressed) and \
            (self.char_shift == self.key_shift_pressed) and \
            (self.char_alt == self.key_alt_pressed) and \
            (self.char_ctrl == self.key_ctrl_pressed)

    def event_handler(self, event: EventType):
        if self.status == STATUS.ACTIVE:
            if event.type == pygame.KEYDOWN:
                # print(f"Char: event_handler: KEYDOWN: {self.char_str}: {event.key}")
                if event.key in KEYS_SHIFT: self.key_shift_pressed = True
                if event.key in KEYS_ALT:   self.key_alt_pressed = True
                if event.key in KEYS_CTRL:  self.key_ctrl_pressed = True

                if is_char(event.key):
                    self.key_code_pressed = event.key
                    self.key_pres_time = datetime.now()
                    # print(f"Char: KEY DOWN: {self.char_str}, Key:  {event.key}")

            # if event.type == pygame.KEYUP:
            #     if event.key in KEYS_SHIFT: self.key_shift_pressed = False
            #     if event.key in KEYS_ALT:   self.key_alt_pressed = False
            #     if event.key in KEYS_CTRL:  self.key_ctrl_pressed = False
            #
            #     if self.char_code == event.key:
            #         self.key_code_pressed = False
            #         self.key_pres_time = None
            #         print(f"KEY UP: {self.char_str}: {event.key}")

    @property
    def green_delta(self):
        return self._green_delta

    @property
    def failed_delta(self):
        return self._failed_delta

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value == STATUS.ACTIVE:
            self._active_start = datetime.now()
        if value == STATUS.SUCCESS:
            self._active_end = datetime.now()
            self._green_delta = self._active_end - self._active_start
            # print(f'GREEN: {self._green_delta.total_seconds()} ts, {self._green_delta.seconds} s, {self._green_delta.microseconds} mks')
        if value == STATUS.FAILED:
            self._active_end = datetime.now()
            self._failed_delta = self._active_end - self._active_start
            # print(f'FAILED: {self._failed_delta.total_seconds()} ts, {self._failed_delta.seconds} s, {self._failed_delta.microseconds} mks')
        self._status = value


INDEX_CHAR = 0
INDEX_CODE = 1
INDEX_SHIFT = 2
INDEX_ALT = 3
INDEX_CTRL = 4
INDEX_LAYOUT = 5
INDEX_PX = 6
INDEX_PY = 7

char_templates = [
    # Char, Code,  Shift, Alt, Ctrl, Layout, x, y #
    [" ", pygame.K_SPACE, 0, 0, 0, KB_LAYOUT_EN, 469, 666],

    ["q", pygame.K_q, 0, 0, 0, KB_LAYOUT_EN], ["Q", pygame.K_q, 1, 0, 0, KB_LAYOUT_EN],
    ["w", pygame.K_w, 0, 0, 0, KB_LAYOUT_EN], ["W", pygame.K_w, 1, 0, 0, KB_LAYOUT_EN],
    ["e", pygame.K_e, 0, 0, 0, KB_LAYOUT_EN], ["E", pygame.K_e, 1, 0, 0, KB_LAYOUT_EN],
    ["r", pygame.K_r, 0, 0, 0, KB_LAYOUT_EN], ["R", pygame.K_r, 1, 0, 0, KB_LAYOUT_EN],
    ["t", pygame.K_t, 0, 0, 0, KB_LAYOUT_EN], ["T", pygame.K_t, 1, 0, 0, KB_LAYOUT_EN],
    ["y", pygame.K_y, 0, 0, 0, KB_LAYOUT_EN], ["Y", pygame.K_y, 1, 0, 0, KB_LAYOUT_EN],
    ["u", pygame.K_u, 0, 0, 0, KB_LAYOUT_EN], ["U", pygame.K_u, 1, 0, 0, KB_LAYOUT_EN],
    ["i", pygame.K_i, 0, 0, 0, KB_LAYOUT_EN], ["I", pygame.K_i, 1, 0, 0, KB_LAYOUT_EN],
    ["o", pygame.K_o, 0, 0, 0, KB_LAYOUT_EN], ["O", pygame.K_o, 1, 0, 0, KB_LAYOUT_EN],
    ["p", pygame.K_p, 0, 0, 0, KB_LAYOUT_EN], ["P", pygame.K_p, 1, 0, 0, KB_LAYOUT_EN],
    ["[", pygame.K_LEFTBRACKET, 0, 0, 0, KB_LAYOUT_EN, 767, 521], ["{", pygame.K_LEFTBRACKET, 1, 0, 0, KB_LAYOUT_EN, 767, 521],
    ["]", pygame.K_RIGHTBRACKET, 0, 0, 0, KB_LAYOUT_EN, 823, 521], ["}", pygame.K_RIGHTBRACKET, 1, 0, 0, KB_LAYOUT_EN, 823, 521],

    ["a", pygame.K_a, 0, 0, 0, KB_LAYOUT_EN], ["A", pygame.K_a, 1, 0, 0, KB_LAYOUT_EN],
    ["s", pygame.K_s, 0, 0, 0, KB_LAYOUT_EN], ["S", pygame.K_s, 1, 0, 0, KB_LAYOUT_EN],
    ["d", pygame.K_d, 0, 0, 0, KB_LAYOUT_EN], ["D", pygame.K_d, 1, 0, 0, KB_LAYOUT_EN],
    ["f", pygame.K_f, 0, 0, 0, KB_LAYOUT_EN], ["F", pygame.K_f, 1, 0, 0, KB_LAYOUT_EN],
    ["g", pygame.K_g, 0, 0, 0, KB_LAYOUT_EN], ["G", pygame.K_g, 1, 0, 0, KB_LAYOUT_EN],
    ["h", pygame.K_h, 0, 0, 0, KB_LAYOUT_EN], ["H", pygame.K_h, 1, 0, 0, KB_LAYOUT_EN],
    ["j", pygame.K_j, 0, 0, 0, KB_LAYOUT_EN], ["J", pygame.K_j, 1, 0, 0, KB_LAYOUT_EN],
    ["k", pygame.K_k, 0, 0, 0, KB_LAYOUT_EN], ["K", pygame.K_k, 1, 0, 0, KB_LAYOUT_EN],
    ["l", pygame.K_l, 0, 0, 0, KB_LAYOUT_EN], ["L", pygame.K_l, 1, 0, 0, KB_LAYOUT_EN],

    ["z", pygame.K_z, 0, 0, 0, KB_LAYOUT_EN], ["Z", pygame.K_z, 1, 0, 0, KB_LAYOUT_EN],
    ["x", pygame.K_x, 0, 0, 0, KB_LAYOUT_EN], ["X", pygame.K_x, 1, 0, 0, KB_LAYOUT_EN],
    ["c", pygame.K_c, 0, 0, 0, KB_LAYOUT_EN], ["C", pygame.K_c, 1, 0, 0, KB_LAYOUT_EN],
    ["v", pygame.K_v, 0, 0, 0, KB_LAYOUT_EN], ["V", pygame.K_v, 1, 0, 0, KB_LAYOUT_EN],
    ["b", pygame.K_b, 0, 0, 0, KB_LAYOUT_EN], ["B", pygame.K_b, 1, 0, 0, KB_LAYOUT_EN],
    ["n", pygame.K_n, 0, 0, 0, KB_LAYOUT_EN], ["N", pygame.K_n, 1, 0, 0, KB_LAYOUT_EN],
    ["m", pygame.K_m, 0, 0, 0, KB_LAYOUT_EN], ["M", pygame.K_m, 1, 0, 0, KB_LAYOUT_EN],

    [";", pygame.K_SEMICOLON, 0, 0, 0, KB_LAYOUT_EN],
    ["'", pygame.K_QUOTE, 0, 0, 0, KB_LAYOUT_EN],
    ["\\", pygame.K_BACKSLASH, 0, 0, 0, KB_LAYOUT_EN],

    ["ё", pygame.K_BACKQUOTE, 0, 0, 0, KB_LAYOUT_RU, 135, 481], ["Ё", pygame.K_BACKQUOTE, 1, 0, 0, KB_LAYOUT_RU, 135, 481],

    ["1", pygame.K_1, 0, 0, 0, KB_LAYOUT_RU, 190, 479], ["!", pygame.K_1, 1, 0, 0, KB_LAYOUT_RU, 190, 479],
    ["2", pygame.K_2, 0, 0, 0, KB_LAYOUT_RU, 244, 479], ["\"", pygame.K_2, 1, 0, 0, KB_LAYOUT_RU, 244, 479],
    ["3", pygame.K_3, 0, 0, 0, KB_LAYOUT_RU, 297, 479], ["№", pygame.K_3, 1, 0, 0, KB_LAYOUT_RU, 297, 479],
    ["4", pygame.K_4, 0, 0, 0, KB_LAYOUT_RU, 351, 479], [";", pygame.K_4, 1, 0, 0, KB_LAYOUT_RU, 351, 479],
    ["5", pygame.K_5, 0, 0, 0, KB_LAYOUT_RU, 403, 479], ["%", pygame.K_5, 1, 0, 0, KB_LAYOUT_RU, 403, 479],
    ["6", pygame.K_6, 0, 0, 0, KB_LAYOUT_RU, 458, 479], [":", pygame.K_6, 1, 0, 0, KB_LAYOUT_RU, 458, 479],
    ["7", pygame.K_7, 0, 0, 0, KB_LAYOUT_RU, 510, 479], ["?", pygame.K_7, 1, 0, 0, KB_LAYOUT_RU, 510, 479],
    ["8", pygame.K_8, 0, 0, 0, KB_LAYOUT_RU, 565, 479], ["*", pygame.K_8, 1, 0, 0, KB_LAYOUT_RU, 565, 479],
    ["9", pygame.K_9, 0, 0, 0, KB_LAYOUT_RU, 617, 479], ["(", pygame.K_9, 1, 0, 0, KB_LAYOUT_RU, 617, 479],
    ["0", pygame.K_0, 0, 0, 0, KB_LAYOUT_RU, 671, 479], [")", pygame.K_0, 1, 0, 0, KB_LAYOUT_RU, 671, 479],
    ["-", pygame.K_MINUS, 0, 0, 0, KB_LAYOUT_RU, 722, 479], ["_", pygame.K_MINUS, 1, 0, 0, KB_LAYOUT_RU, 722, 479],

    ["й", pygame.K_q, 0, 0, 0, KB_LAYOUT_RU, 207, 521], ["Й", pygame.K_q, 1, 0, 0, KB_LAYOUT_RU, 207, 521],
    ["ц", pygame.K_w, 0, 0, 0, KB_LAYOUT_RU, 263, 521], ["Ц", pygame.K_w, 1, 0, 0, KB_LAYOUT_RU, 263, 521],
    ["у", pygame.K_e, 0, 0, 0, KB_LAYOUT_RU, 317, 521], ["У", pygame.K_e, 1, 0, 0, KB_LAYOUT_RU, 317, 521],
    ["к", pygame.K_r, 0, 0, 0, KB_LAYOUT_RU, 376, 521], ["К", pygame.K_r, 1, 0, 0, KB_LAYOUT_RU, 376, 521],
    ["е", pygame.K_t, 0, 0, 0, KB_LAYOUT_RU, 432, 521], ["Е", pygame.K_t, 1, 0, 0, KB_LAYOUT_RU, 432, 521],
    ["н", pygame.K_y, 0, 0, 0, KB_LAYOUT_RU, 487, 521], ["Н", pygame.K_y, 1, 0, 0, KB_LAYOUT_RU, 487, 521],
    ["г", pygame.K_u, 0, 0, 0, KB_LAYOUT_RU, 544, 521], ["Г", pygame.K_u, 1, 0, 0, KB_LAYOUT_RU, 544, 521],
    ["ш", pygame.K_i, 0, 0, 0, KB_LAYOUT_RU, 600, 521], ["Ш", pygame.K_i, 1, 0, 0, KB_LAYOUT_RU, 600, 521],
    ["щ", pygame.K_o, 0, 0, 0, KB_LAYOUT_RU, 655, 521], ["Щ", pygame.K_o, 1, 0, 0, KB_LAYOUT_RU, 655, 521],
    ["з", pygame.K_p, 0, 0, 0, KB_LAYOUT_RU, 711, 521], ["З", pygame.K_p, 1, 0, 0, KB_LAYOUT_RU, 711, 521],
    ["х", pygame.K_LEFTBRACKET, 0, 0, 0, KB_LAYOUT_RU, 767, 521], ["Х", pygame.K_LEFTBRACKET, 1, 0, 0, KB_LAYOUT_RU, 767, 521],
    ["ъ", pygame.K_RIGHTBRACKET, 0, 0, 0, KB_LAYOUT_RU, 823, 521], ["Ъ", pygame.K_RIGHTBRACKET, 1, 0, 0, KB_LAYOUT_RU, 823, 521],

    ["ф", pygame.K_a, 0, 0, 0, KB_LAYOUT_RU, 201, 566], ["Ф", pygame.K_a, 1, 0, 0, KB_LAYOUT_RU, 201, 566],
    ["ы", pygame.K_s, 0, 0, 0, KB_LAYOUT_RU, 260, 566], ["Ы", pygame.K_s, 1, 0, 0, KB_LAYOUT_RU, 260, 566],
    ["в", pygame.K_d, 0, 0, 0, KB_LAYOUT_RU, 319, 566], ["В", pygame.K_d, 1, 0, 0, KB_LAYOUT_RU, 319, 566],
    ["а", pygame.K_f, 0, 0, 0, KB_LAYOUT_RU, 378, 566], ["А", pygame.K_f, 1, 0, 0, KB_LAYOUT_RU, 378, 566],
    ["п", pygame.K_g, 0, 0, 0, KB_LAYOUT_RU, 438, 566], ["П", pygame.K_g, 1, 0, 0, KB_LAYOUT_RU, 438, 566],
    ["р", pygame.K_h, 0, 0, 0, KB_LAYOUT_RU, 495, 566], ["Р", pygame.K_h, 1, 0, 0, KB_LAYOUT_RU, 495, 566],
    ["о", pygame.K_j, 0, 0, 0, KB_LAYOUT_RU, 554, 566], ["О", pygame.K_j, 1, 0, 0, KB_LAYOUT_RU, 554, 566],
    ["л", pygame.K_k, 0, 0, 0, KB_LAYOUT_RU, 612, 566], ["Л", pygame.K_k, 1, 0, 0, KB_LAYOUT_RU, 612, 566],
    ["д", pygame.K_l, 0, 0, 0, KB_LAYOUT_RU, 672, 566], ["Д", pygame.K_l, 1, 0, 0, KB_LAYOUT_RU, 672, 566],
    ["ж", pygame.K_SEMICOLON, 0, 0, 0, KB_LAYOUT_RU, 729, 566], ["Ж", pygame.K_SEMICOLON, 1, 0, 0, KB_LAYOUT_RU, 729, 566],
    ["э", pygame.K_QUOTE, 0, 0, 0, KB_LAYOUT_RU, 787, 566], ["Э", pygame.K_QUOTE, 1, 0, 0, KB_LAYOUT_RU, 787, 566],

    ["я", pygame.K_z, 0, 0, 0, KB_LAYOUT_RU, 219, 614], ["Я", pygame.K_z, 1, 0, 0, KB_LAYOUT_RU, 219, 614],
    ["ч", pygame.K_x, 0, 0, 0, KB_LAYOUT_RU, 278, 614], ["Ч", pygame.K_x, 1, 0, 0, KB_LAYOUT_RU, 278, 614],
    ["с", pygame.K_c, 0, 0, 0, KB_LAYOUT_RU, 342, 614], ["С", pygame.K_c, 1, 0, 0, KB_LAYOUT_RU, 342, 614],
    ["м", pygame.K_v, 0, 0, 0, KB_LAYOUT_RU, 402, 614], ["М", pygame.K_v, 1, 0, 0, KB_LAYOUT_RU, 402, 614],
    ["и", pygame.K_b, 0, 0, 0, KB_LAYOUT_RU, 466, 614], ["И", pygame.K_b, 1, 0, 0, KB_LAYOUT_RU, 466, 614],
    ["т", pygame.K_n, 0, 0, 0, KB_LAYOUT_RU, 527, 614], ["Т", pygame.K_n, 1, 0, 0, KB_LAYOUT_RU, 527, 614],
    ["ь", pygame.K_m, 0, 0, 0, KB_LAYOUT_RU, 588, 614], ["Ь", pygame.K_m, 1, 0, 0, KB_LAYOUT_RU, 588, 614],
    ["б", pygame.K_COMMA, 0, 0, 0, KB_LAYOUT_RU, 649, 614], ["Б", pygame.K_COMMA, 1, 0, 0, KB_LAYOUT_RU, 649, 614],
    ["ю", pygame.K_PERIOD, 0, 0, 0, KB_LAYOUT_RU, 710, 614], ["Ю", pygame.K_PERIOD, 1, 0, 0, KB_LAYOUT_RU, 710, 614],
    [".", pygame.K_SLASH, 0, 0, 0, KB_LAYOUT_RU, 774, 614], [",", pygame.K_SLASH, 1, 0, 0, KB_LAYOUT_RU, 774, 614],

    ["/", pygame.K_BACKSLASH, 0, 0, 0, KB_LAYOUT_RU, 890, 520]

]


def mark_char_one(char: str, count: int = None, max_count: int = None, factor: float = None, color: Color = COLOR.HELP_KEY):  # factor = count / max_count
    """
    Рисует на клавиатуре эллипс для маркировки символа
    :param char: str -- Символ
    :param count: int -- Количество таких символов в тексте
    :param max_count: int -- Всего символов в тексте
    :param factor: float -- Коэффициент масштабирования маркера = count / max_count
    :param color: Цвет маркера
    :return: None -- Ничего не возвращает
    """
    k: float  # коэффициент размера, обратный частоте использования символа
    if factor is not None:
        k = factor
    else:
        if count is None: count = 1
        if max_count is None: max_count = 1
        k = count / max_count

    for t in char_templates:
        if t[INDEX_CHAR] == char:
            w_max, w_min = 40, 12
            h_max, h_min = 30, 9
            w = (w_max - w_min) * k + w_min
            h = (h_max - h_min) * k + h_min
            r = pygame.Rect(0, 0, w, h)
            # print(f"char: {char} {t}[{INDEX_PX}], t[{INDEX_PY}]")
            r.center = t[INDEX_PX], t[INDEX_PY]
            pygame.draw.ellipse(surface=SCREEN, color=color, rect=r, width=0)
            return
    raise Exception(f"chars.py: mark_char_on_keyboard(char: str): \n"
                    f"Критическая ошибка: Символ [{char}] не найден.")


def mark_char_line(char_line: str, is_words: bool = False, weights: list | None = None, color: Color = COLOR.HELP_KEY):
    """
    Маркирует (рисует кружочки) на клавиатуре все символы строки
    :param char_line: строка символов
    :param is_words: bool -- Рассматривать строку как слово, т.е. не сортировать и не считать символы.
    :param weights: List[int] -- список весовых значений слов
    :return:
    """
    sorted_list: list = []
    max_count: int = 1
    if is_words:
        if weights is None:
            l: int = len(char_line)
            max_count = l+2
            for i in range(l):
                sorted_list.append([char_line[i], l - i])
        else:
            if len(char_line) == len(weights):
                for i in range(len(char_line)):
                    sorted_list.append([char_line[i], weights[i]])
            else:
                raise Exception(f"При указании массива weights \n"
                                f"количество символов в входной строке {len(char_line)} \n"
                                f"и количество элементов в массиве weights {len(weights)} \n"
                                f"должно быть одинаковым.")
    else:
        sorted_chars = sorted(char_line)
        sorted_string = ''.join(sorted_chars)
        processed_char: str = ''
        processed_count: int = 0
        for c in sorted_string:
            if processed_char == c:
                processed_count += 1
                if processed_count > max_count:
                    max_count = processed_count
            else:
                if processed_char != '':
                    sorted_list.append([processed_char, processed_count])
                processed_char = c
                processed_count = 1
        if processed_char != '':
            sorted_list.append([processed_char, processed_count])
        # if max_count == 0:
        #     print("MAX_COUNT = 0: ", char_line)

    for rec in sorted_list:
        mark_char_one(char=rec[0], count=rec[1], max_count=max_count, color=color)


def is_char(key_code: int) -> bool:
    for t in char_templates:
        if t[INDEX_CODE] == key_code:  # Code
            return True
    return False


def get_char(char_str: str) -> OneChar:
    for t in char_templates:
        if t[INDEX_CHAR] == char_str:
            return OneChar(char_str=t[INDEX_CHAR], key_code=t[INDEX_CODE], key_shift=(t[INDEX_SHIFT] == 1),
                           key_alt=(t[INDEX_ALT] == 1), key_ctrl=(t[INDEX_CTRL] == 1), kb_layout=t[INDEX_LAYOUT],
                           kb_px=t[INDEX_PX], kb_py=t[INDEX_PY])
    print_color(f"chars.py: get_char(char_str: str): \n"
                f"Критическая ошибка: Символ [{char_str}] не найден.", CONSOLE_COLORS["red"])
    exit(10)
