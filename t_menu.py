import pygame.event

from chars import mark_char_line
from globals import *


class TMenu:
    def __init__(self, rect: RectType, conf: list, selected: int = 0):
        self.status: int = STATUS.ACTIVE
        self.screen: pygame.Surface = SCREEN
        self.rect: RectType = rect
        self.conf: list = conf
        self.lessons_count = len(self.conf["lessons"])
        self.font: pygame.font.Font = get_font_default(None, 22)
        self.cell_spacing: int = 3
        self.cell_v_padding: int = 5
        self.cell_h_padding: int = 10
        self.item_text_color: tuple = COLOR.MENU_TEXT
        self.item_box_color_sel: tuple = COLOR.MENU_BK_SELECTED
        self.selected_index: int = selected
        self.img_do_training_yes: pygame.Surface = pygame.image.load("img/menu/do_training_yes.png")
        self.img_do_training_no: pygame.Surface = pygame.image.load("img/menu/do_training_no.png")
        self.w_speed: int = 0
        self.h_speed: int = 0
        self.w_rating: int = 0
        self.h_rating: int = 0
        self.w_name: int = 0
        self.h_name: int = 0
        self.w_probes: int = 0
        self.h_probes: int = 0
        font_probes: pygame.font.Font = get_font_default(font_size=18)
        for lesson in self.conf["lessons"]:
            lesson["img_speed"]: pygame.Surface = self.font.render(str(int(lesson["speed"])), ANTIALIASING, self.item_text_color)
            if self.w_speed < lesson["img_speed"].get_width(): self.w_speed = lesson["img_speed"].get_width()
            if self.h_speed < lesson["img_speed"].get_height(): self.h_speed = lesson["img_speed"].get_height()
            lesson["img_rating"]: pygame.Surface = self.font.render(str(int(lesson["rating"])), ANTIALIASING, self.item_text_color)
            if self.w_rating < lesson["img_rating"].get_width(): self.w_rating = lesson["img_rating"].get_width()
            if self.h_rating < lesson["img_rating"].get_height(): self.h_rating = lesson["img_rating"].get_height()
            lesson["img_name"]: pygame.Surface = self.font.render(str(lesson["name"]), ANTIALIASING, self.item_text_color)
            if self.w_name < lesson["img_name"].get_width(): self.w_name = lesson["img_name"].get_width()
            if self.h_name < lesson["img_name"].get_height(): self.h_name = lesson["img_name"].get_height()
            lesson["img_probes"]: pygame.Surface = font_probes.render(str(int(lesson["ok_training"])), ANTIALIASING, COLOR.BLACK80)
            if self.w_probes < lesson["img_probes"].get_width(): self.w_probes = lesson["img_probes"].get_width()
            if self.h_probes < lesson["img_probes"].get_height(): self.h_probes = lesson["img_probes"].get_height()
        self.item_width = (
                self.cell_h_padding + max(self.img_do_training_yes.get_width(), self.img_do_training_no.get_width()) +  # [X]
                self.cell_h_padding + self.w_name +  # Имя урока
                self.cell_h_padding + self.w_speed +  # Результирующая скорость
                self.cell_h_padding + self.w_rating +  # Результирующий рейтинг
                self.cell_h_padding + self.w_probes + self.cell_h_padding)  # Количество прохождений урока
        self.item_height = self.cell_v_padding + max(self.h_name, self.h_speed, self.h_rating, self.h_probes) + self.cell_v_padding
        self.key_down: bool = False
        self.key_time_down: datetime | None = None
        self.key_time_last_action: datetime | None = None
        self.last_action: int | None = None

    def graw_item(self, px: int, py: int, lesson: list, selected: bool):

        #     "name": "ао",
        #     "do_training": true,
        #     "ok_training": 1,
        #     "rating": 152.58265567449345,
        #       /\
        #    +----------------------------------------------+
        #    | [X] имя_урока  скорость  рейтинг колич_проб  |
        #    +----------------------------------------------+

        rect_item: RectType = RectType(px, py, self.item_width, self.item_height)

        if lesson['do_training']:
            img_do: pygame.Surface = self.img_do_training_yes
        else:
            img_do: pygame.Surface = self.img_do_training_no
        rect_do: RectType = img_do.get_rect()
        rect_do.x = px + self.cell_h_padding
        rect_do.centery = rect_item.centery

        rect_name: RectType = lesson['img_name'].get_rect()
        rect_name.x = px + self.cell_h_padding + rect_do.width + self.cell_h_padding
        rect_name.centery = rect_item.centery

        rect_speed: RectType = lesson['img_speed'].get_rect()
        rect_speed.right = px + self.cell_h_padding + rect_do.width + self.cell_h_padding + self.w_name + self.cell_h_padding + self.w_speed
        rect_speed.centery = rect_item.centery

        rect_rating: RectType = lesson['img_rating'].get_rect()
        rect_rating.right = rect_speed.right + self.cell_h_padding + self.w_rating
        rect_rating.centery = rect_item.centery

        rect_probes: RectType = lesson['img_probes'].get_rect()
        rect_probes.right = rect_rating.right + self.cell_h_padding + self.w_probes
        rect_probes.centery = rect_item.centery

        if selected:
            pygame.draw.rect(self.screen, self.item_box_color_sel, rect_item, 0, 3)
        else:
            pygame.draw.rect(self.screen, self.item_box_color_sel, rect_item, 1, 3)
        self.screen.blit(img_do, rect_do)
        self.screen.blit(lesson['img_name'], rect_name)
        self.screen.blit(lesson['img_speed'], rect_speed)
        self.screen.blit(lesson['img_rating'], rect_rating)
        self.screen.blit(lesson['img_probes'], rect_probes)

    def draw(self):
        count_on_rect = self.rect.height // (self.item_height + self.cell_spacing)
        if self.lessons_count > count_on_rect:
            index_top: int = self.selected_index - (count_on_rect // 2)
            if index_top < 0:
                index_top = 0
            index_bottom = index_top + count_on_rect - 1
            if index_bottom > (self.lessons_count - 1):
                index_bottom = self.lessons_count - 1
                index_top = index_bottom - count_on_rect + 1
        else:
            index_top = 0
            index_bottom = len(self.conf["lessons"]) - 1

        h_visible_menu = count_on_rect * (self.item_height + self.cell_spacing) - self.cell_spacing
        dy = (self.rect.height - h_visible_menu) // 2
        px: int = self.rect.x + (self.rect.width - self.item_width) // 2
        py: int = self.rect.y + dy

        for index in range(index_top, index_bottom + 1, 1):

            if index_top > 0:
                pygame.draw.polygon(surface=SCREEN,
                                    color=COLOR.GREEN,
                                    points=[(self.rect.x + CHAR_WIDTH * 1.5, self.rect.y),
                                            (self.rect.x + CHAR_WIDTH * 2, self.rect.y + 7),
                                            (self.rect.x + CHAR_WIDTH, self.rect.y + 7)])

            if index_bottom < (self.lessons_count - 1):
                pygame.draw.polygon(surface=SCREEN,
                                    color=COLOR.GREEN,
                                    points=[(self.rect.right - CHAR_WIDTH * 1.5, self.rect.bottom),
                                            (self.rect.right - CHAR_WIDTH * 2, self.rect.bottom - 7),
                                            (self.rect.right - CHAR_WIDTH, self.rect.bottom - 7)])

            if index == self.selected_index:
                self.graw_item(px, py, self.conf["lessons"][index], True)
                if ("str" in self.conf["lessons"][index]) and (len(self.conf["lessons"][index]["str"]) > 0):
                    mark_char_line(self.conf["lessons"][index]["str"])
                elif len(self.conf["lessons"][index]["fixed_str"]) > 0:
                    mark_char_line(self.conf["lessons"][index]["fixed_str"])
                else:
                    mark_char_line(self.conf["lessons"][index]["generate_str"])
            else:
                self.graw_item(px, py, self.conf["lessons"][index], False)
            py += self.item_height + self.cell_spacing

    def do_training_change_state(self):
        self.conf["lessons"][self.selected_index]["do_training"] = not self.conf["lessons"][self.selected_index]["do_training"]

    def do_training_set_state(self, state: bool):
        for l in self.conf["lessons"]:
            l["do_training"] = state

    def get_do_training_count(self) -> int:
        count: int = 0
        for l in self.conf["lessons"]:
            if l["do_training"]:
                count += 1
        return count

    def selector_up(self):
        if self.selected_index > 0:
            self.selected_index -= 1

    def selector_pg_up(self):
        if self.selected_index > 0:
            self.selected_index -= self.rect.height // ((self.item_height + self.cell_spacing) * 2)
        if self.selected_index < 0:
            self.selected_index = 0

    def selector_pg_down(self):
        self.selected_index += self.rect.height // ((self.item_height + self.cell_spacing) * 2)
        if self.selected_index > self.lessons_count - 1:
            self.selected_index = self.lessons_count - 1

    def selector_down(self):
        if self.selected_index < (self.lessons_count - 1):
            self.selected_index += 1

    def selector_home(self):
        self.selected_index = 0

    def selector_end(self):
        self.selected_index = (self.lessons_count - 1)

    def repeat_last_action(self):
        match self.last_action:
            case None:
                pass
            case ACTION.move_up:
                self.selector_up()
            case ACTION.move_down:
                self.selector_down()
            case ACTION.move_pg_up:
                self.selector_pg_up()
            case ACTION.move_pg_down:
                self.selector_pg_down()
            case ACTION.move_home:
                self.selector_home()
            case ACTION.move_end:
                self.selector_end()
            case ACTION.move_left:
                pass
            case ACTION.move_right:
                pass
            case ACTION.change_state:
                self.do_training_change_state()
            case ACTION.act_end:
                self.status = STATUS.END
            case ACTION.act_escape:
                self.status = STATUS.END
                GamePhase.shift_prev()
            case _:
                print_color(f"TMenu.repeat_last_action(). Не обрабатываемое последнее действие \"{self.last_action}\" ",
                            console_color=COLOR.RED)
                GamePhase.phase = Phases.QUIT
                exit(10)

    def update(self):
        if self.key_down:
            if self.key_time_down is None:
                self.key_time_down = datetime.now() + AUTO_REPEAT_WAIT  # установка времени начала повторных нажатий
            if self.key_time_down < datetime.now():  # время начала повторных нажатий
                if self.key_time_last_action is None:
                    self.key_time_last_action = datetime.now()
                if datetime.now() > self.key_time_last_action:
                    self.repeat_last_action()
                    self.key_time_last_action = datetime.now() + AUTO_REPEAT_ON

    def event_handler(self, event: pygame.event.Event):
        if event.type == pygame.KEYUP:
            self.key_down = False
            self.key_time_down = None
            self.key_time_last_action = None

        if event.type == pygame.KEYDOWN:
            self.key_down = True
            # print(f"event: {event}")
            match event.key:
                case pygame.K_RETURN:
                    if self.get_do_training_count() > 0:
                        self.status = STATUS.END
                        self.last_action = None
                case pygame.K_SPACE:
                    self.do_training_change_state()
                    self.last_action = ACTION.change_state
                case pygame.K_UP:
                    self.selector_up()
                    self.last_action = ACTION.move_up
                case pygame.K_DOWN:
                    self.selector_down()
                    self.last_action = ACTION.move_down
                case pygame.K_PAGEDOWN:
                    self.selector_pg_down()
                    self.last_action = ACTION.move_pg_down
                case pygame.K_PAGEUP:
                    self.selector_pg_up()
                    self.last_action = ACTION.move_pg_up
                case pygame.K_LEFT:
                    self.last_action = ACTION.move_left
                    pass
                case pygame.K_RIGHT:
                    self.last_action = ACTION.move_right
                    pass
                case pygame.K_HOME:
                    self.selector_home()
                    self.last_action = ACTION.move_home
                case pygame.K_END:
                    self.selector_end()
                    self.last_action = ACTION.move_end
                case pygame.K_END:
                    self.selector_end()
                    self.last_action = ACTION.move_end
                case pygame.K_MINUS | pygame.K_KP_MINUS:
                    self.do_training_set_state(False)
                    self.last_action = None
                case pygame.K_PLUS | pygame.K_EQUALS | pygame.K_KP_PLUS:
                    self.do_training_set_state(True)
                    self.last_action = None
