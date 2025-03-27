import pygame
from pygame.event import EventType

# from globals import *
from chars import *
from control import Control


class LineChars:

    def __init__(self, line_str: str, is_words: bool = False):
        self.screen: pygame.Surface = SCREEN
        self.time_start: datetime = datetime.now()
        self.line_str: str = line_str
        self.is_words: bool = is_words
        self.line_hints: list[str] = str_to_paragraph(long_str=self.line_str, font=FONT_DEFAULT)
        self.line: list[OneChar] = []
        self.line_count_chars = count_chars(self.line_str)

        char_str: str
        self.word_end_index: int = 0  # индекс конца текущего слова, для отображения на клавиатуре
        # for char_str in line_str:
        for i in range(len(line_str)):
            self.line.append(get_char(char_str=line_str[i]))
            if (self.word_end_index == 0) and (line_str[i] == " "):
                self.word_end_index = i

        self.line[0].status = STATUS.ACTIVE
        self.Y: int = LINE_Y
        self.X1: int = LINE_X1
        self.X2: int = LINE_X2
        self.char_width: int = CHAR_WIDTH  # letter width
        self.char_height: int = CHAR_HEIGHT  # letter height
        self.speed = SPEED_LPM  # LPM letters / min
        CPM: float = self.speed  # chars per min
        CPS: float = CPM / 60  # chars per sec
        PPS: float = CPS * self.char_width  # pixels per sec
        PPD: float = PPS / FPS  # pixels per draw
        self.dx: float = PPD
        self.px: float = self.X2
        self.py: float = self.Y
        self.status: int = STATUS.ACTIVE
        # self.rating: int = 0

    def re_init(self):
        one_char: OneChar
        for one_char in self.line:
            one_char.re_init()
        self.line[0].status = STATUS.ACTIVE
        self.status = STATUS.ACTIVE

    def update(self):
        self.px -= self.dx
        for char in self.line: char.update()
        index = 0
        px_active: float = self.px
        while index < len(self.line):

            # поиск конца следующего слова
            if self.line[index].char_str == " ":
                for i in range(index+1, len(self.line)):
                    if (self.line[index].char_str == " ") or (i == (len(self.line)-1)):
                        self.word_end_index = i
                        break

            px_active += (self.line[index].width + self.char_width)
            if self.line[index].status in [STATUS.FAILED, STATUS.SUCCESS]:
                if (index + 1) < len(self.line):
                    if self.line[index + 1].status == STATUS.QUEUE:
                        self.line[index + 1].status = STATUS.ACTIVE
                else:
                    self.status = STATUS.END
                    # print("LineChars.update: LINE END.")
            elif self.line[index].status == STATUS.ACTIVE:
                # x = self.px + index * CHAR_WIDTH
                if px_active < ((LINE_RECT.left + LINE_RECT.centerx) / 2):
                    self.px += self.dx

            index += 1

    def draw(self):
        index: int = 0
        x: float = self.px
        y: float = self.py
        color_index: int
        while index < len(self.line):
            if self.X1 < x < self.X2:
                self.line[index].draw(px=x, py=y)
            x += (self.line[index].width + self.char_width)
            index += 1
            if x > self.X2:
                break
        # draw_paragraph(paragraph=self.line_hints, color=COLOR.GRAY80)
        draw_chars(line_chars=self, is_text=False)
        if self.is_words:
            index_active: int | None = None
            index_space: int | None = None
            for i in range(len(self.line_str)):
                if index_active is None:
                    if self.line[i].status == STATUS.ACTIVE:
                        index_active = i
                else:
                    if index_space is None:
                        if self.line_str[i] == " ":
                            index_space = i
                            break
            if self.line_str[index_active] != " ":
                mark_char_line(char_line=self.line_str[index_active+1:index_space], is_words=True, color=COLOR.HELP_WORD)

    def event_handler(self, event: EventType):
        # self.control.event_handler(event=event)
        for char in self.line:
            char.event_handler(event)

        # if event.type == pygame.KEYDOWN:
        #     print("KEY: ", event.key)
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     print("BTN: ", event.pos, event.button)
        # if event.type == pygame.MOUSEMOTION:
        #     print("MOV: ", event.pos)


draw_chars_cache_str = ""
draw_chars_cache_par = []


def draw_chars(line_chars: LineChars, is_text: bool, rect: RectType = LINE_RECT):  # line_chars: LineChars
    global draw_chars_cache_str
    global draw_chars_cache_par
    if draw_chars_cache_str == line_chars.line_str:
        paragraph = draw_chars_cache_par
    else:
        one_word = ""
        one_word_width = 0
        one_str = ""
        one_str_width = 0
        paragraph = []
        for char in line_chars.line:
            one_word = one_word + char.char_str
            one_word_width += (CHAR_SPACING + char.width)
            if is_text:
                if char.char_str == " ":
                    one_str = one_str + one_word
                    one_str_width += one_word_width
                    one_word = ""
                    one_word_width = 0
            if one_str_width + one_word_width > (LINE_RECT.width - CHAR_WIDTH * 2):
                # print(one_str)
                # print(one_word)
                # print(f"one_str_width + one_word_width {one_str_width} + {one_word_width} = {one_str_width + one_word_width}")
                if one_str_width > 0:
                    paragraph.append(one_str)
                    one_str = ""
                    one_str_width = 0
                else:
                    paragraph.append(one_word)
                    one_word = ""
                    one_word_width = 0
        # print(one_str)
        # print(one_word)
        # print(f"one_str_width + one_word_width {one_str_width} + {one_word_width} = {one_str_width + one_word_width}")
        if (one_str_width > 0) or (one_word_width > 0):
            paragraph.append(one_str + one_word)
        draw_chars_cache_str = line_chars.line_str
        draw_chars_cache_par = paragraph
        # print(paragraph)

    all_lines: int = len(paragraph)
    visible_lines: int = rect.height // CHAR_HEIGHT
    visible_line1: int = 0  # первая отображаемая линия
    visible_line2: int = all_lines - 1  # последняя отображаемая линия

    if all_lines > visible_lines:
        # ищем в какой строке активный символ
        index: int = 0
        active_line: int = 0
        found: bool = False
        for one_str in paragraph:
            for one_char in one_str:
                if line_chars.line[index].status == STATUS.ACTIVE:
                    found = True
                    break
                index += 1
            if found:
                break
            active_line += 1
        if active_line > (visible_lines - 1):
            visible_line1 = active_line - visible_lines + 1
        visible_line2 = visible_line1 + visible_lines - 1
        # print(all_lines, visible_lines, visible_line1, active_line, visible_line2)

    if visible_line1 > 0:
        pygame.draw.polygon(surface=SCREEN,
                            color=COLOR.GREEN,
                            points=[(rect.x + CHAR_WIDTH * 1.5, rect.y),
                                    (rect.x + CHAR_WIDTH * 2, rect.y + 7),
                                    (rect.x + CHAR_WIDTH, rect.y + 7)])
    if visible_line2 < (all_lines - 1):
        pygame.draw.polygon(surface=SCREEN,
                            color=COLOR.GREEN,
                            points=[(rect.right - CHAR_WIDTH * 1.5, rect.bottom),
                                    (rect.right - CHAR_WIDTH * 2, rect.bottom - 7),
                                    (rect.right - CHAR_WIDTH, rect.bottom - 7)])

    one_str_len: float
    index = 0
    py = rect.centery - ((visible_line2 - visible_line1) / 2) * CHAR_HEIGHT  # + CHAR_HEIGHT / 2
    current_draw_line = 0  # текущая отображаемая линия
    for one_str in paragraph:
        if visible_line1 <= current_draw_line <= visible_line2:
            # -------- чтобы выравнивать по центру ---------
            # one_str_len = (len(one_str) - 1) * CHAR_SPACING
            # for index_str in range(0, len(one_str) - 1):
            #     one_str_len += line_chars.line[index + index_str].width
            # px = rect.centerx - one_str_len / 2
            # ----------------------------------------------
            px = rect.x + CHAR_WIDTH
            for one_char in one_str:
                line_chars.line[index].draw(px=px, py=py)
                px += (CHAR_SPACING + line_chars.line[index].width)
                index += 1
            py += CHAR_HEIGHT
        else:
            index += len(one_str)
        current_draw_line += 1
