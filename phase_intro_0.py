from pygame.draw_py import Point

import globals
import military_object
from mo_bullet import Bullet
from globals import *
from image_fly import *
from show_images import ShowImages
from phase_init import get_dict_words_counter
from t_simple_scroller import TSimpleScroller
from t_table import TTable


def game_phase_intro_0():
    menu = [
        {"speed": 100,
         "text": "До 100 знаков в минуту – Довольно слабый показатель. Вам нужно учиться печатать более быстро, иначе всем придется ждать, пока Вы наберете "
                 "нужный текст."},
        {"speed": 200,
         "text": "От 100 до 200 знаков в минуту – Средний показатель. Вы неплохо набираете тексты на клавиатуре, но все равно еще рано расслабляться. Ваш "
                 "показатель уже приближается к оптимальному, осталось еще чуть-чуть поработать."},
        {"speed": 300,
         "text": "От 200 до 300 знаков в минуту – Хороший показатель. Вы довольно быстро набираете тексты на клавиатуре, что не может не радовать. Наверное, "
                 "Вы уже написали не одну сотню страниц в различных текстовых редакторах."},
        {"speed": 400,
         "text": "От 300 до 400 знаков в минуту – Отличный показатель. Вашей скорости печати на клавиатуре можно позавидовать. Такой скоростью набора текста "
                 "владеют люди, которым часто приходиться набирать различные тексты на клавиатуре."},
        {"speed": 600,
         "text": "Свыше 400 знаков в минуту – Просто великолепно. Если Ваша скорость набора на клавиатуре превышает 400 знаков в минуту, то Вы просто гений "
                 "клавиатурного набора. На свете таких людей вряд ли больше 1 процента."},
        {"speed": 800,
         "text": "Ну и напоследок. Если Ваша скорость набора текста на клавиатуре составляет свыше 750 знаков в минуту, то Вам пора обратиться в книгу "
                 "Рекордов Гиннесса. Потому что именно такой рекорд был установлен в 2005 году."},
    ]

    images = [
        pygame.image.load("img/intro_0/intro_0.png")
    ]
    img_rect = images[0].get_rect()
    img_rect.center = SCREEN_W / 2, SCREEN_H / 2

    count_paragraph = len(menu)
    margin = 10
    w = (SCREEN_H - MARGIN_H * 2 - margin * count_paragraph) / count_paragraph
    h = SCREEN_H - MARGIN_H * 2
    # font_size = 22
    # font: pygame.font.Font = pygame.font.Font(None, font_size)
    # i_fly: ImageFly = ImageFly(image=pygame.image.load("img/end/depositphotos_2976601-stock-illustration-ok-emoticon.png"))

    if len(globals.ALL_WORDS) == 0:
        SCREEN.fill(COLOR.BK)
        SCREEN.blit(images[0], img_rect)
        pygame.display.flip()

        conf = read_conf(CONF_LESSONS)
        globals.SEVERITY_ERRORS = conf["SEVERITY_ERRORS"]
        word_length: FromTo = FromTo(2, conf["WORD_LENGTH"])

        os.chdir(BOOKS_DIR)
        words: dict | None = read_words_dict(conf["WORDS"])
        if words is not None:
            globals.ALL_WORDS = words
        else:
            for fn in conf["BOOKS"]:
                content = read_file(fn)
                print(f"Файл {fn} прочитали. Длина {len(content)} символов")
                globals.ALL_WORDS = get_dict_words_counter(
                    stage_str=content,
                    stage_dict=globals.ALL_WORDS,
                    word_len=word_length,
                    debug_search=None,  # debug_search=["ст", "сти"]
                    gscroller=TSimpleScroller(title=fn, rect=RectType(200, SCREEN_H - 65, SCREEN_W - 400, 40), value_start=0, value_end=len(content))
                )
                with open(conf["WORDS"], 'w', encoding='utf-8') as outfile:
                    json.dump(globals.ALL_WORDS, outfile, indent=2, ensure_ascii=False)
        os.chdir("..")

        print(f"Длина словаря: {len(globals.ALL_WORDS)}")
        max_f: int = max(globals.ALL_WORDS.values())
        print("Наибольшая частота: {}".format(max_f))

    while GamePhase.phase == Phases.INTRO_0:
        r: pygame.Rect = pygame.Rect(MARGIN_W, MARGIN_H, h, w)
        if time_to_draw_screen():
            SCREEN.fill(COLOR.BK)
            military_object.run_step()
            SCREEN.blit(images[0], img_rect)
            # i_fly.update()
            # i_fly.draw()

            # for s in menu:
            #     paragraph = str_to_paragraph(long_str=s["text"], font=font, rect=r)
            #     r.h = font_size * len(paragraph)
            #     draw_paragraph(paragraph=paragraph, color=COLOR.MENU,
            #                    rect=r, font=font)
            #
            #     pygame.draw.rect(surface=SCREEN, rect=r, color=COLOR.MENU, width=1)
            #     r.top = r.top + r.h + margin
            pygame.display.flip()
            for event in pygame.event.get():
                if check_quit(event=event):
                    GamePhase.shift_prev()
                    break

                if event.type == pygame.KEYDOWN:
                    # print(F"game_phase_intro_0. event:  {event}")
                    if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        # print(F"game_phase_intro_0. GAME_PHASE: {GAME_PHASE} -> {PHASE.GAME_PRE_RUN}")
                        GamePhase.shift_next()
