import pygame

from globals import *


class ListMenu:
    def __init__(self, rect: pygame.Rect, items: list, default_index: int = None, default_name: str = None,
                 color_text: tuple = COLOR.MENU_TEXT,
                 color_text_selected: tuple = COLOR.MENU_TEXT_SELECTED,
                 color_bk: tuple = COLOR.MENU_BK,
                 color_border: tuple = COLOR.MENU_BORDER,
                 border: int = 1,  # if border == 0, (default) fill the rectangle
                 # if border > 0, used for line thickness
                 # if border < 0, nothing will be drawn
                 border_radius: int = 5,
                 border_top_left_radius: int = -1,
                 border_top_right_radius: int = -1,
                 border_bottom_left_radius: int = -1,
                 border_bottom_right_radius: int = -1,
                 padding: int = 5,
                 font_size: int = 24
                 ):
        self.screen: pygame.Surface = SCREEN
        self.status: int = STATUS.PASSIVE
        self.rect: pygame.Rect = rect
        self.font: pygame.font.Font = pygame.font.Font(None, 30)
        self.items: list = items

        if (default_index is not None) and (0 <= default_index < len(self.items)):
            self.index: int = default_index
        else:
            self.index: int = 0

        if default_name is not None:
            self.index = self.items.index(default_name)
        else:
            self.line_str: str = default_name

        self.color_text: tuple = color_text
        self.color_text_selected: tuple = color_text_selected
        self.color_bk: tuple = color_bk
        self.color_border: tuple = color_border
        self.border: int = border
        self.border_radius: int = border_radius
        self.border_top_left_radius: int = border_top_left_radius
        self.border_top_right_radius: int = border_top_right_radius
        self.border_bottom_left_radius: int = border_bottom_left_radius
        self.border_bottom_right_radius: int = border_bottom_right_radius
        self.font_size: int = font_size
        self.font: pygame.font.Font = get_font_default(font_size=self.font_size)
        self.padding: int = padding

        self.items_img: list = []
        self.items_img_empty: pygame.Surface = None
        self.item_H: int = 0
        if len(self.items) > 0:
            for item in self.items:
                self.items_img.append([
                    self.font.render(item, ANTIALIASING, self.color_text),
                    self.font.render(item, ANTIALIASING, self.color_text_selected)
                ])
            self.item_H = self.items_img[0][0].get_height()
        else:
            self.items_img_empty = self.font.render("<< тут ничего нет... >>", ANTIALIASING, self.color_text)
            self.item_H = self.items_img_empty.get_height()

    def draw(self):
        px = self.rect.left + self.padding
        py = self.rect.top + self.padding

        if self.status == STATUS.ACTIVE:
            pygame.draw.rect(surface=self.screen, color=COLOR.BORDER_ACTIVE, rect=self.rect,
                             width=self.border,
                             border_radius=self.border_radius,
                             border_top_left_radius=self.border_top_left_radius,
                             border_top_right_radius=self.border_top_right_radius,
                             border_bottom_left_radius=self.border_bottom_left_radius,
                             border_bottom_right_radius=self.border_bottom_right_radius)
        else:
            pygame.draw.rect(surface=self.screen, color=COLOR.BORDER_PASSIVE, rect=self.rect,
                             width=self.border,
                             border_radius=self.border_radius,
                             border_top_left_radius=self.border_top_left_radius,
                             border_top_right_radius=self.border_top_right_radius,
                             border_bottom_left_radius=self.border_bottom_left_radius,
                             border_bottom_right_radius=self.border_bottom_right_radius)

        r: pygame.Rect = pygame.Rect(px, py, self.rect.width - self.padding * 2, self.item_H)
        if len(self.items) > 0:
            for (index, item_img) in enumerate(self.items_img):
                if index != self.index:
                    self.screen.blit(item_img[0], r)
                else:
                    self.screen.blit(item_img[1], r)
                r.top += self.item_H + self.padding
        else:
            self.screen.blit(self.items_img_empty, r)

    def update(self):
        if len(self.items) > 0:
            # if self.index < 0:
            #     self.index = len(self.items) - 1
            # if self.index >= len(self.items):
            #     self.index = 0
            self.line_str = self.items[self.index]

    def event_handler(self, event: EventType):
        if len(self.items) > 0 and self.status == STATUS.ACTIVE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_HOME:
                    self.index = 0
                if event.key == pygame.K_END:
                    self.index = len(self.items) - 1
                if event.key == pygame.K_UP:
                    if self.index > 0:
                        self.index -= 1
                    else:
                        self.index = len(self.items) - 1
                if event.key == pygame.K_DOWN:
                    if self.index < (len(self.items)-1):
                        self.index += 1
                    else:
                        self.index = 0
                if event.key in [pygame.K_KP_ENTER, pygame.KSCAN_KP_ENTER]:
                    self.line_str = self.items[self.index]
                    self.status = STATUS.END

            # if event.type == pygame.KEYUP:
            #     if event.key in KEYS_SHIFT: self.key_shift_pressed = False
            #     if event.key in KEYS_ALT:   self.key_alt_pressed = False
            #     if event.key in KEYS_CTRL:  self.key_ctrl_pressed = False
            #
            #     if self.char_code == event.key:
            #         self.key_code_pressed = False
            #         self.key_pres_time = None
            #         print(f"KEY UP: {self.char_str}: {event.key}")

        self.update()
    # ----------------------------------------------------------------------
