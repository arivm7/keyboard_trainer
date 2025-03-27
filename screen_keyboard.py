from globals import *


class ScreenKeyboard:

    def __init__(self, screen: pygame.Surface = SCREEN):
        self.screen = screen

        self.img_texts: pygame.Surface = pygame.image.load("img/kb/kb_texts.png")  # Надписи на клавиатуре
        self.img_hands: pygame.Surface = pygame.image.load("img/kb/kb_hands.png")  # Руки
        self.img_places: pygame.Surface = pygame.image.load("img/kb/kb_fingers_places.png")  # Места постановки пальцев
        self.img_plastic: pygame.Surface = pygame.image.load("img/kb/kb_plastik.png")  # Пластик
        self.rect: pygame.Rect = None
        # self.rect.bottom = self.screen.get_rect().bottom
        # print(f"KB: RECT: {self.rect}")

    def update(self):
        pass

    def draw(self, phase: int):

        match phase:
            case Phases.PRE | Phases.MID:
                # Прямоугольник для вывода текста
                pygame.draw.rect(surface=self.screen, color=COLOR.BLACK90, rect=LINE_RECT, border_radius=10)
                pygame.draw.rect(surface=self.screen, color=COLOR.BLACK60, rect=LINE_RECT, width=1, border_radius=10)

                self.rect = self.img_plastic.get_rect()
                self.rect.midbottom = self.screen.get_rect().midbottom
                self.screen.blit(self.img_plastic, self.rect)
                self.screen.blit(self.img_places, self.rect)
            case Phases.POST:
                self.rect = self.img_plastic.get_rect()
                self.rect.midbottom = self.screen.get_rect().midbottom
                self.screen.blit(self.img_texts, self.rect)
            case Phases.CHOOSE_LESSONS:
                # Прямоугольник для вывода текста
                pygame.draw.rect(surface=self.screen, color=COLOR.BLACK90, rect=LINE_RECT, border_radius=10)
                pygame.draw.rect(surface=self.screen, color=COLOR.BLACK60, rect=LINE_RECT, width=1, border_radius=10)

                self.rect = self.img_plastic.get_rect()
                self.rect.midbottom = self.screen.get_rect().midbottom
                self.screen.blit(self.img_plastic, self.rect)
            case Phases.GAME_RESULT:
                self.rect = self.img_plastic.get_rect()
                self.rect.midbottom = self.screen.get_rect().midbottom
                self.screen.blit(self.img_plastic, self.rect)
                self.screen.blit(self.img_texts, self.rect)
            case Phases.INTRO_1:
                self.rect = self.img_plastic.get_rect()
                self.rect.midbottom = self.screen.get_rect().midbottom
                self.screen.blit(self.img_plastic, self.rect)
                self.screen.blit(self.img_texts, self.rect)
                self.screen.blit(self.img_hands, self.rect)
            case Phases.INTRO_2:
                self.rect = self.img_plastic.get_rect()
                self.rect.midbottom = self.screen.get_rect().midbottom
                self.screen.blit(self.img_plastic, self.rect)
                self.screen.blit(self.img_places, self.rect)
                self.screen.blit(self.img_texts, self.rect)
            case _:
                print_color(
                    f"ScreenKeyboard.draw: \nКритическая ошибка: Неизвестная фаза для отрисовки: [Phases.{phase}]",
                    CONSOLE_COLORS["red"])
                exit(10)

        btn_sx, btn_sy = 67.7, 67.8
        x1 = 37
        L1y = 390.9
        #     ~   !            @            #            $            %            ^            &            *            (            )             _             +             Bs
        #     `   1            2            3            4            5            6            7            8            9            0             -             =             Bs
        #     37  104.7        172.4        240.1        307.8        375.5        443.2        510.9        578.6        646.3        714.0         781.7         849.4         917.1
        #     390.9
        L1 = [x1, x1 + btn_sx * 1, x1 + btn_sx * 2, x1 + btn_sx * 3, x1 + btn_sx * 4, x1 + btn_sx * 5, x1 + btn_sx * 6,
              x1 + btn_sx * 7, x1 + btn_sx * 8, x1 + btn_sx * 9, x1 + btn_sx * 10, x1 + btn_sx * 11, x1 + btn_sx * 12,
              x1 + btn_sx * 13]
        # for L1x in L1: pygame.draw.circle(self.screen, color=COLOR.GRAY40, center=[L1x, L1y], radius=btn_sx/2-5, width=3)

        L2y = L1y + btn_sy
        x2 = 75
        #    Tab    Q            W            E            R            T            Y            U            I            O            P            {            }            |
        #    Tab    q            w            e            r            t            y            u            i            o            p            [            ]            \
        #    Tab    Й            Ц            У            К            Е            Н            Г            Ш            Щ            З            Х            Ъ            /
        #    Tab    й            ц            у            к            е            н            г            ш            щ            з            х            ъ            \
        # X   75    142.7        210.4        278.1        345.8        413.5        481.2        548.9        616.6        684.3        752.0        819.7        887.4        955.1
        # Y   458.7
        L2 = [x2, x2 + btn_sx * 1, x2 + btn_sx * 2, x2 + btn_sx * 3, x2 + btn_sx * 4, x2 + btn_sx * 5, x2 + btn_sx * 6,
              x2 + btn_sx * 7, x2 + btn_sx * 8, x2 + btn_sx * 9, x2 + btn_sx * 10, x2 + btn_sx * 11, x2 + btn_sx * 12,
              x2 + btn_sx * 13]
        # for L2x in L2: pygame.draw.circle(self.screen, color=COLOR.GRAY40, center=[L2x, L2y], radius=btn_sx/2-5, width=3)

        L3y = L2y + btn_sy
        x3 = 86
        #    Caps   A            S            D            F            G            H            J            K            L            :            "            Enter
        #    Caps   a            s            d            f            g            h            j            k            l            ;            '            Enter
        #           Ф            Ы            В            А            П            Р            О            Л            Д            Ж            Э
        #           ф            ы            в            а            п            р            о            л            д            ж            э
        # X  86     153.7        221.4        289.1        356.8        424.5        492.2        559.9        627.6        695.3        763.0        830.7        898.4
        # Y  526.5
        L3 = [x3, x3 + btn_sx * 1, x3 + btn_sx * 2, x3 + btn_sx * 3, x3 + btn_sx * 4, x3 + btn_sx * 5, x3 + btn_sx * 6,
              x3 + btn_sx * 7, x3 + btn_sx * 8, x3 + btn_sx * 9, x3 + btn_sx * 10, x3 + btn_sx * 11, x3 + btn_sx * 12]
        # for L3x in L3: pygame.draw.circle(self.screen, color=COLOR.GRAY40, center=[L3x, L3y], radius=btn_sx/2-5, width=3)

        L4y = L3y + btn_sy
        x4 = 121.3
        #     Shift        Z            X            C            V            B            N            M            <            >            ?            Shift
        #     Shift        z            x            c            v            b            n            m            ,            .            /            Shift
        #                  Я            Ч            С            М            И            Т            Ь            Б            Ю            ,
        #                  я            ч            с            м            и            т            ь            б            ю            .
        #     121.3        189.0        256.7        324.4        392.1        459.8        527.5        595.2        662.9        730.6        798.3        866.0
        # Y   594.3
        L4 = [x4, x4 + btn_sx * 1, x4 + btn_sx * 2, x4 + btn_sx * 3, x4 + btn_sx * 4, x4 + btn_sx * 5, x4 + btn_sx * 6,
              x4 + btn_sx * 7, x4 + btn_sx * 8, x4 + btn_sx * 9, x4 + btn_sx * 10, x4 + btn_sx * 11]
        # for L4x in L4: pygame.draw.circle(self.screen, color=COLOR.GRAY40, center=[L4x, L4y], radius=btn_sx/2-5, width=3)

        L5y = L4y + btn_sy
        #     Ctrl      Win        Alt        Space      Alt        Fn         Menu       Ctrl
        # X   50        138        229        467        705        796        883        977
        # Y   662.1
        L5 = [50, 138, 229, 467, 705, 796, 883, 977]
        # for L5x in L5: pygame.draw.circle(self.screen, color=COLOR.GRAY40, center=[L5x, L5y], radius=btn_sx/2-5, width=3)

        #     print(L5x)
        # print(L5y)
        # exit(1)

        # Линия, по которой бежит текст
        pygame.draw.line(self.screen, COLOR.BLACK60, (LINE_X1, LINE_Y + CHAR_HEIGHT / 2),
                         (LINE_X2, LINE_Y + CHAR_HEIGHT / 2))

        # for c in char_templates:
        #     #      [" ", pygame.K_SPACE, 0, 0, 0, KB_LAYOUT_EN, 469, 696],
        #     if len(c) == 8:
        #         r = pygame.Rect(0, 0, 40, 30)
        #         r.center = c[6], c[7]
        #         pygame.draw.ellipse(surface=self.screen, color=COLOR.HELP, rect=r, width=0)


keyboard: ScreenKeyboard = ScreenKeyboard()
