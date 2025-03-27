import random
from collections import namedtuple

from pygame.rect import RectType

from globals import read_file, COUNT_WORDSET_FOR_USE_WEIGHT, FromTo, WORD_LENGTH, SCREEN_H, SCREEN_W
from t_simple_scroller import TSimpleScroller

WordCount = namedtuple('WordCount', ['word', 'count'])
ListWordCount = list[WordCount]
SCROLLER_DEFAULT = FromTo(1, 90)

COUNT_LESSON_PER_ONE_CHARSET: int = 3  # Количество уроков для одного набора символов
COUNT_WORD_PER_LESSON: int = 25  # Количество слов в уроке
# WORD_LENGTH: FromTo = FromTo(2, 10)  # Диапазон длин слов для уроков

SPEED_CPM = 100  # char per minute. Рекомендуемая скорость
TIME_ONE_LESSON = 60  # in seconds. Время одного урока при рекомендуемой скорости

file_names: list[str] = [
    # "books/Толстой Л. - Война и мир.txt",
    # "books/Николай Федоров - Философия общего дела (Философские технологии).txt",
    # "books/Ильин Иван - Россия. Путь к возрождению (Русские мыслители).txt",
    "books/Достоевский Ф. - ПСС в 35 томах. Том 3 - 2014.txt",
    "books/Достоевский Ф. - ПСС в 35 томах. Том 4 - 2015.txt"
]

excludes = [  # список буквосочетаний, которые не есть словами и их не нужно сохранять в список
    "ббк",
    "гг",
    "ге",
    "гей",
    "гн",
    "кн",
    "ооо",
    "см",
    "спб",
    "ст",
    "ти",
    "шй",
    "удк",
    "ргб",
    "ниор",
    "лн"
]

char_sets = [
    "ёйцук ен гшщзхъ",
    "фыва пр олджэ",
    "ячсм ит ьбю",
    "камепи нртгоь",
    "епимакувс нртьогшлб",
    "епимакувсчыц нртьогшлбюдщ",
    "епимакувсчыцйфя нртьогшлбюдщзжэхъ",
]


def is_letter(one_char: str):
    letters: str = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    return one_char in letters


def get_dict_words_counter(stage_str: str,  # Входная строка
                           stage_dict: dict | None = None,  # Дополняемый словарь. В него пишутся данные выборки
                           word_len: FromTo = None,  # Длина выбираемых слов
                           tscroller: FromTo | None = None,  # SCROLLER_DEFAULT -- Длина индикатора выполнения
                           debug_search: list[str] | None = None,  # Поиск указанных слов с выводом строки и номера символа во входном тексте
                           gscroller: TSimpleScroller | None = None
                           ) -> dict:
    """
    Разбор текстовой строки на слова с подсчетом количества вхождений этого слова.
    Возвращает словарь: (слово: количество)
    Записи добавляются в словарь stage_dict, он-же возвращается
    т.е. может дополнять внешний словарь
    :param stage_str:  Входная строка
    :param stage_dict: Дополняемый словарь. В него пишутся данные выборки
    :param word_len: Длина выбираемых слов
    :param tscroller: Длина текстового индикатора выполнения
    :param debug_search: Поиск указанных слов с выводом строки и номера символа во входном тексте
    :param gscroller: TSimpleScroller -- Графический скроллер
    :return: возвращает stage_dict дополненный словами из входной строки
    """
    if stage_dict is None: stage_dict = {}

    scroller_len: int = 1
    if tscroller is not None:
        scroller_len = tscroller.t - tscroller.f + 1
        # dict_counter: dict = {}
        s: str = "Выборка-слов"
        print(f"|-{s}", end="")
        i = tscroller.f + 1
        while i < tscroller.t - 2 - len(s):
            print("-", end="")
            i += 1
        print(">|")

    scroller_point: float = len(stage_str) / scroller_len
    point_index: int = 0
    word: str = ""
    char: str
    char_index: int = 1
    line_index: int = 1
    for i in range(len(stage_str)):
        char = stage_str[i].lower()
        char_index += 1
        if char == chr(10):
            line_index += 1
            char_index = 0
        if is_letter(char):
            word = word + char
        else:
            if len(word) > 0:
                if (word_len is None) or ((word_len.f <= len(word)) and (len(word) <= word_len.t)):
                    d = stage_dict.get(word, 0) + 1
                    if word not in excludes:
                        if debug_search is not None:
                            if word in debug_search:
                                print(f"DEBUG: {word}: {line_index} {char_index}")
                        stage_dict.update([(word, d)])
                word = ""
        if gscroller is not None:
            gscroller.value = i
            gscroller.draw(True)
        if tscroller is not None:
            point_index += 1
            if point_index >= scroller_point:
                print("#", end="")
                point_index = 0

    if len(word) > 0:
        d = stage_dict.get(word, 0) + 1
        if word not in excludes:
            stage_dict.update([(word, d)])
    if gscroller is not None:
        gscroller.value = gscroller.value_end
        gscroller.draw(True)
    if tscroller is not None:
        print("#")
    return stage_dict


def chars_in_set(search: str, stage: str) -> bool:
    """
    Возвращает Истину если все символы искомой строки search входят в строку stage
    :param search: искомые символы. Если они все входят в stage, то Истина
    :param stage: базовое множество в которое должны входить все искомые символы
    :return: Истина/Ложь
    """
    for c in search:
        if c not in stage:
            return False
    return True


def get_sort_list(dict_counter: dict, scroller: FromTo = SCROLLER_DEFAULT) -> list[WordCount]:
    """
    Удаление элементов из словаря и перемещение их в список в отсортированном виде
    :param dict_counter: исходный словарь. При завершении остаётся пустым.
    :param scroller: Параметры отображения скроллера на кране, поскольку операция длительная.
    :return: Отсортированный массив (слово, количество) по убыванию количества.
    """
    scroller_len: int = scroller.t - scroller.f + 1
    scroller_point: float = len(dict_counter) / scroller_len

    s: str = "Сортировка"
    print(f"|-{s}", end="")
    i = scroller.f + 1
    while i < scroller.t - 2 - len(s):
        print("-", end="")
        i += 1
    print(">|")

    list_sorted: list = []
    index: int = 0
    while len(dict_counter) > 0:
        max_value = max(dict_counter.values())
        for k, v in dict_counter.items():
            if v == max_value:
                dict_counter.pop(k)
                list_sorted.append(WordCount(word=k, count=v))
                break
        index += 1
        if index >= scroller_point:
            print("#", end="")
            index = 0
    print("#")
    return list_sorted


def get_words_by_chars(stage_list: ListWordCount = None, stage_dict: dict = None, included_chars: str = None) -> ListWordCount:
    """
    Возвращает list с парами (Слово: количество)
    :param stage_list: ListWordCount -- полный список слов в виде списка (обычно сортированный)
    :param stage_dict: dict -- полный список слов в виде словаря
    :param included_chars: str -- список символов, которые должны входить в выбранные слова
    :return: ListWordCount -- список слов только содержащих символы из строки included_chars
    """
    word_set: ListWordCount = []
    if stage_list is not None:
        for w in stage_list:
            if (included_chars is None) | (chars_in_set(w.word, included_chars)):
                word_set.append(w)
    if stage_dict is not None:
        for k, v in stage_dict.items():
            if (included_chars is None) | (chars_in_set(k, included_chars)):
                word_set.append(WordCount(word=k, count=v))
    return word_set


def get_lesson(word_set: ListWordCount, count_word: int | None = None, count_chars: int | None = None, use_weight: bool | None = None) -> str:
    """
    Формирование строки для урока в клавиатурном тренажёре
    :param word_set: список слов с количествами
    :param count_word: количество слов в уроке
    :param count_chars: количество символов в уроке
    :param use_weight: использовать ли количество слов как вероятность использования слова
    :return: строка со списком слов
    """
    if (count_word is None) and (count_chars is None):
        raise Exception("count_word и count_chars не определены. Генерация строки не возможна. Должен быть определен кто-то из них")

    lesson_str: str = ""
    words: list = []
    weights: list = []
    weight: list | None = None

    for d in word_set:
        words.append(d.word)
        weights.append(d.count)

    match use_weight:
        case True:
            weight = weights
        case False:
            weight = None
        case None:
            if len(word_set) > COUNT_WORDSET_FOR_USE_WEIGHT:
                weight = weights
            else:
                weight = None

    if count_word is not None:
        lesson_list: list = random.choices(words, weights=weight, k=count_word)
        lesson_str = ' '.join(lesson_list)

    if count_chars is not None:
        while len(lesson_str) < count_chars:
            if len(lesson_str) > 0:
                lesson_str += " "
            lesson_str += random.choices(words, weights=weight, k=1)[0]

    return lesson_str


if __name__ == '__main__':
    dict_all_word_count: dict = {}
    for fn in file_names:
        content = read_file(fn)
        print(f"Файл {fn} прочитали. Длина {len(content)} символов")
        dict_all_word_count = get_dict_words_counter(
            stage_str=content, stage_dict=dict_all_word_count, word_len=WORD_LENGTH, debug_search=["смо", "заба"],  # debug_search=["ст", "сти"]
            gscroller=TSimpleScroller(title=fn, rect=RectType(200, SCREEN_H - 100, SCREEN_W - 400, 50), value_start=0, value_end=len(content))
            )
        print(f"Длина словаря: {len(dict_all_word_count)}")
    max_f: int = max(dict_all_word_count.values())
    print("Наибольшая частота: {}".format(max_f))

    list_sorted: list[WordCount] | None = None
    # list_sorted = get_sort_list(dict_all_word_count)

    # выбрать слова с указанным набором символов
    word_sets: list[ListWordCount] = []
    for char_set in char_sets:
        word_set: ListWordCount
        if list_sorted is not None:
            word_set = get_words_by_chars(stage_list=list_sorted, stage_dict=None, included_chars=char_set)
        else:
            word_set = get_words_by_chars(stage_list=None, stage_dict=dict_all_word_count, included_chars=char_set)
        word_sets.append(word_set)

    for word_set in word_sets:
        print("----------------------------------------------------------------------------------------------")
        print("Длина словаря {} записей".format(len(word_set)))
        for i in range(COUNT_LESSON_PER_ONE_CHARSET):
            print(get_lesson(word_set=word_set, count_word=COUNT_WORD_PER_LESSON, use_weight=len(word_set) > COUNT_WORDSET_FOR_USE_WEIGHT))

    # print("==============================================================================================")
    # for word_set in word_sets:
    #     print("----------------------------------------------------------------------------------------------")
    #     for d in word_set:
    #         # print("{:20} {}".format(d.word, d.count))
    #         pass

    # print(hash("вафываыва"))
