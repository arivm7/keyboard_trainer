import pygame.font

from chars import is_char
from globals import *


class Layout:
    INDEX_ID = 0
    INDEX_TITLE = 1
    INDEX_COLOR = 2
    def __init__(self,
                 px: int = SCREEN_W - 30,
                 py: int = SCREEN_H - 200,
                 layouts: list[[]] = [
                     [KB_LAYOUT_EN, "EN", COLOR.BLUE],
                     [KB_LAYOUT_RU, "RU", COLOR.RED]
                 ],
                 keys: list[[]] = [KEYS_ALT, KEYS_SHIFT]
                 ):
        self.screen: pygame.Surface = SCREEN
        self.px: int = px
        self.py: int = py
        self.layouts: list[[]] = layouts
        self.keys: list[[]] = keys
        self.index: int = 0
        self.index_last: int = self.index
        self.font: pygame.font.Font = FONT_DEFAULT
        self.layout: int = None
        self.id: int = None
        self.title: str = None
        self.img: pygame.Surface = None
        self.rect: pygame.Rect = None
        self.update_layout()

    def update_layout(self):
        self.layout = self.layouts[self.index]
        self.id = self.layout[self.INDEX_ID]
        self.title: str = self.layout[self.INDEX_TITLE]
        self.img = self.font.render(self.title, ANTIALIASING, self.layout[self.INDEX_COLOR])
        self.rect = self.img.get_rect()

    def draw(self):
        self.rect.center = self.px, self.py
        self.screen.blit(self.img, self.rect)

    def event_handler(self, event: EventType):
        if event.type == pygame.KEYDOWN:
            # print(f"Char: event_handler: KEYDOWN: {self.char_str}: {event.key}")
            for k in self.keys:
                if event.key in KEYS_SHIFT: self.key_shift_pressed = True
                if event.key in KEYS_ALT:   self.key_alt_pressed = True
                if event.key in KEYS_CTRL:  self.key_ctrl_pressed = True

            if is_char(event.key):
                self.key_code_pressed = event.key
                self.key_pres_time = datetime.now()
                print(f"Char: KEY DOWN: {self.char_str}, Key:  {event.key}")
