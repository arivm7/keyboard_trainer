import military_object
from globals import *
from screen_keyboard import keyboard


def game_phase_intro_2():

    hint = [
        "Приготовьтесь:",
        "Установите пальцы на указанные места",
        "и нажмите любую кнопку",
        "для начала игры"
    ]

    while GamePhase.phase == Phases.INTRO_2:
        if time_to_draw_screen():
            SCREEN.fill(COLOR.BK)
            military_object.run_step()
            keyboard.draw(Phases.INTRO_2)
            draw_paragraph(paragraph=hint, color=COLOR.GREEN, rect=LINE_RECT)
            pygame.display.flip()
            for event in pygame.event.get():
                if check_quit(event):
                    GamePhase.shift_prev()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # mouse_pos_x, mouse_pos_y = event.pos
                    print("MOUSE BTN DN: ", event.pos)
                if event.type == pygame.KEYDOWN:
                    # print(F"game_phase_intro_2. event:  {event}")
                    # print(F"game_phase_intro_2. GAME_PHASE: {GAME_PHASE} -> {PHASE.GAME_PRE_RUN}")
                    # if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    GamePhase.shift_next()

