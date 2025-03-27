import pygame

from chars import is_char
from globals import *


class InputLine:
    def __init__(self, rect: pygame.Rect, default_name: str, font_size: int = 30):
        self.screen: pygame.Surface = SCREEN
        self.status: int = STATUS.ACTIVE
        self.rect: pygame.Rect = rect
        self.font: pygame.font.Font = pygame.font.Font(None, font_size)
        self.line_str: str = default_name
        self.cursor_index: int = len(self.line_str)
        self.img_label: pygame.Surface = self.font.render("Имя: ", ANTIALIASING, COLOR.LABEL)
        self.margin: int = 5
        self.border_radius: int = 5

    def draw(self):
        if self.status == STATUS.ACTIVE:
            pygame.draw.rect(surface=self.screen, color=COLOR.BORDER_ACTIVE, rect=self.rect, width=1, border_radius=self.border_radius)
        else:
            pygame.draw.rect(surface=self.screen, color=COLOR.BORDER_PASSIVE, rect=self.rect, width=1, border_radius=self.border_radius)

        px = self.rect.left + self.margin
        py = self.rect.top + self.margin
        r: pygame.Rect = self.img_label.get_rect()
        r.topleft = px, py
        self.screen.blit(self.img_label, r)
        px += r.width
        s1: str
        s2: str
        if self.cursor_index > 0:
            s1 = self.line_str[:self.cursor_index]
        else:
            s1 = ""
        if self.cursor_index < len(self.line_str):
            s2 = self.line_str[self.cursor_index:]
        else:
            s2 = ""
        if len(s1) > 0:
            img = self.font.render(s1, ANTIALIASING, COLOR.NAME)
            r = img.get_rect()
            r.topleft = px, py
            self.screen.blit(img, r)
            px += r.width

        # курсор старт
        if self.status == STATUS.ACTIVE:
            r = pygame.Rect(px, py, 2, r.height)
            pygame.draw.rect(surface=self.screen, color=COLOR.CURSOR, rect=r)
            # px += r.width
        # курсор енд

        if len(s2) > 0:
            img = self.font.render(s2, ANTIALIASING, COLOR.NAME)
            r: pygame.Rect = img.get_rect()
            r.topleft = px, py
            self.screen.blit(img, r)
            px += r.width

    def event_handler(self, event: EventType):
        if self.status == STATUS.ACTIVE:
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_HOME:
                        self.cursor_index = 0
                    if event.key == pygame.K_END:
                        self.cursor_index = len(self.line_str)
                    if event.key == pygame.K_LEFT:
                        if self.cursor_index > 0:
                            self.cursor_index -= 1
                    if event.key == pygame.K_RIGHT:
                        if self.cursor_index < len(self.line_str):
                            self.cursor_index += 1
                    if event.key == pygame.K_BACKSPACE:
                        if self.cursor_index > 0:
                            self.cursor_index -= 1
                            self.line_str = self.line_str[:self.cursor_index] + self.line_str[self.cursor_index + 1:]
                    if event.key == pygame.K_DELETE:
                        if self.cursor_index < len(self.line_str):
                            self.line_str = self.line_str[:self.cursor_index] + self.line_str[self.cursor_index + 1:]

                #  game_phase_pre_run. event:  <Event(768-KeyDown {'unicode': 'Ы', 'key': 115, 'mod': 4097, 'scancode': 22, 'window': None})>
                if is_char(event.key):
                    if self.cursor_index < len(self.line_str):
                        self.line_str = self.line_str[:self.cursor_index] + event.unicode + self.line_str[self.cursor_index:]
                    else:
                        self.line_str = self.line_str + event.unicode
                    self.cursor_index += 1

            # if event.type == pygame.KEYUP:
            #     if event.key in KEYS_SHIFT: self.key_shift_pressed = False
            #     if event.key in KEYS_ALT:   self.key_alt_pressed = False
            #     if event.key in KEYS_CTRL:  self.key_ctrl_pressed = False
            #
            #     if self.char_code == event.key:
            #         self.key_code_pressed = False
            #         self.key_pres_time = None
            #         print(f"KEY UP: {self.char_str}: {event.key}")

