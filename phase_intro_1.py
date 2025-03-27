import military_object
from globals import *
from screen_keyboard import keyboard


def game_phase_intro_1():

    hint = [
        "Расположите пальцы на кнопках",
        "как показано на рисунке ниже",
        "и нажмите любую кнопку"
    ]

    while GamePhase.phase == Phases.INTRO_1:
        if time_to_draw_screen():
            SCREEN.fill(COLOR.BK)
            military_object.run_step()
            keyboard.draw(GamePhase.INTRO_1)
            draw_paragraph(paragraph=hint, color=COLOR.GREEN, rect=LINE_RECT)
            pygame.display.flip()
            for event in pygame.event.get():
                if check_quit(event):
                    GamePhase.shift_prev()
                    break
                if event.type == pygame.KEYDOWN:
                    # print(F"game_phase_intro_1. event:  {event}")
                    # print(F"game_phase_intro_1. GAME_PHASE: {GAME_PHASE} -> {PHASE.GAME_PRE_RUN}")
                    # if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    GamePhase.shift_next()
