from globals import *


class ShowImages:

    def __init__(self, folder: str = "img/final/01",  # /01-0030.png
                 px: int = LINE_RECT.centerx,
                 py: int = LINE_RECT.centery,
                 fps: int = 30,
                 repeat: bool = False,
                 screen: pygame.Surface = SCREEN):
        # self.folder: str = folder
        self.screen: pygame.Surface = screen
        self.status: int = STATUS.ACTIVE
        self.repeat: bool = repeat
        self.frameWait: float = 1000 / fps  # milliseconds / frame
        self.frameTimeNext: datetime = datetime.now()

        # print("show_images: init: Считывание картинок")
        prev_folder = os.getcwd()
        # print(f"show_images: init: Исходная папка: {prev_folder}")
        os.chdir(folder)
        # print(f"show_images: init: Папка с изображениями: {folder}")
        if not os.path.isdir(folder):
            raise Exception("show_images: init: Критическая ошибка. Папки с картинками нет.")
        dir_list = os.listdir(folder)
        dir_list.sort()
        self.images = []  # pygame.image.load("img/final/01/01-0030.png")
        for file_name in dir_list:
            self.images.append(pygame.image.load(file_name))
        os.chdir(prev_folder)
        # print(f"show_images: init: Вернулись в исходную папку: {os.getcwd()}")

        self.imagesCount = len(self.images)
        # print(f"show_images: init: Подгружено картинок: {self.imagesCount}")
        self.imageIndex: int | None = None
        self.image: pygame.Surface | None = None
        self.rect: RectType | None = None
        self.image_next()
        self.px: float = px
        self.py: float = py
        self.rect.centerx = self.px
        self.rect.centery = self.py

    def image_next(self):
        now: datetime = datetime.now()
        if self.frameTimeNext <= now:
            self.frameTimeNext = now + timedelta(milliseconds=self.frameWait)
            if self.imageIndex < self.imagesCount - 1:
                self.imageIndex += 1
                self.image = self.images[self.imageIndex]
                self.rect = self.image.get_rect()
            else:
                if self.repeat:
                    self.imageIndex = 0
                else:
                    self.status = STATUS.END

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.image_next()

    def event_handler(self, event: EventType):
        if self.status == STATUS.ACTIVE:
            if event.type == pygame.KEYDOWN:
                self.status = STATUS.END
