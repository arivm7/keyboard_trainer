from t_cell import *


class TTable:
    def __init__(self,
                 table_rec: list[list[dict]],  # массив ячеек таблицы в виде словаря
                 cell_spacing: int = 5,  # отступ между ячейками
                 cell_padding: int = 5,  # отступ внутри ячейки до текста
                 cell_h_align: int = ALIGN.LEFT,  # Горизонтальное выравнивание
                 cell_v_align: int = ALIGN.CENTER,  # вертикальное выравнивание
                 cell_text_color: tuple = COLOR.TEXT_DEFAULT,
                 bk_color: tuple = COLOR.BK_DEFAULT,
                 frame_width: int = 1,
                 frame_color: tuple = COLOR.TEXT_DEFAULT,
                 font: pygame.font.Font = FONT_DEFAULT):

        self.screen: pygame.Surface = SCREEN
        # self.table_str: list = table_str
        self.cell_spacing: int = cell_spacing
        self.cell_padding: int = cell_padding
        self.cell_h_align: int = cell_h_align
        self.cell_v_align: int = cell_v_align
        self.cell_text_color: tuple = cell_text_color
        self.bk_color: tuple = bk_color
        self.frame_width: int = frame_width
        self.frame_color: tuple = frame_color
        self.font: pygame.font.Font = font

        self.rows: int = len(table_rec)  # количество строк
        self.cols: int = 0  # количество колонок
        for row in table_rec:
            c = len(row)
            if c > self.cols: self.cols = c

        # массив высот строк
        self.h_rows: list = []
        for i_row in range(0, self.rows, 1):
            self.h_rows.insert(i_row, 0)

        # массив ширины колонок
        self.w_cols: list = []
        for i_col in range(0, self.cols, 1):
            self.w_cols.insert(i_col, 0)

        # формирование индексов массива
        self.cells: list[list[TCell | None]] = []
        for i_row in range(0, self.rows, 1):
            self.cells.insert(i_row, [])
            for i_col in range(0, self.cols, 1):
                self.cells[i_row].insert(i_col, None)

        # рендерим ячейки
        for i_row in range(0, self.rows, 1):
            for i_col in range(0, self.cols, 1):
                self.cells[i_row][i_col] = TCell(text_str=table_rec[i_row][i_col].get("text"),
                                                 padding=table_rec[i_row][i_col].get("padding", self.cell_padding),
                                                 h_align=table_rec[i_row][i_col].get("h_align", self.cell_h_align),
                                                 v_align=table_rec[i_row][i_col].get("v_align", self.cell_v_align),
                                                 text_color=table_rec[i_row][i_col].get("text_color", self.cell_text_color),
                                                 bk_color=table_rec[i_row][i_col].get("bk_color", self.bk_color),
                                                 font=table_rec[i_row][i_col].get("font", self.font),
                                                 frame_width=table_rec[i_row][i_col].get("frame_width", 0), # self.frame_width
                                                 frame_color=table_rec[i_row][i_col].get("frame_color", None)) # self.frame_color
                # print(f"table_str[{i_row}][{i_col}] {table_str[i_row][i_col]}")
                r: RectType = self.cells[i_row][i_col].rect()
                if self.w_cols[i_col] < r.width: self.w_cols[i_col] = r.width
                if self.h_rows[i_row] < r.height: self.h_rows[i_row] = r.height

        # ширина всей таблицы
        self.width: int = self.cell_spacing
        for i_col in range(0, self.cols, 1): self.width += (self.w_cols[i_col] + self.cell_spacing)

        # высота всей таблицы
        self.height: int = self.cell_spacing
        for i_row in range(0, self.rows, 1): self.height += (self.h_rows[i_row] + self.cell_spacing)

        # рект всей таблицы
        self.rect: RectType = RectType(0, 0, self.width, self.height)

    def get_rect_cell(self, index_col: int, index_row: int) -> RectType:
        """
        Возвращает rect для вывода указанной ячейки
        :param index_col: индекс колонки, начиная с "0"
        :param index_row: индекс строки, начиная с "0"
        :return: rect для вывода этой ячейки
        """
        px: int = self.rect.x + self.cell_spacing
        py: int = self.rect.y + self.cell_spacing
        for i_col in range(0, index_col, 1): px += (self.w_cols[i_col] + self.cell_spacing)
        for i_row in range(0, index_row, 1): py += (self.h_rows[i_row] + self.cell_spacing)
        return RectType(px, py, self.w_cols[index_col], self.h_rows[index_row])

    def draw(self):

        # подложка ячейки
        if self.bk_color is not None:
            pygame.draw.rect(self.screen, self.bk_color, self.rect, width=0)

        # рамка ячейки
        if self.frame_width > 0:
            pygame.draw.rect(self.screen, self.frame_color, self.rect, width=self.frame_width)

        for i_row in range(0, self.rows, 1):
            for i_col in range(0, self.cols, 1):
                cell_rect = self.get_rect_cell(index_col=i_col, index_row=i_row)
                pygame.draw.rect(self.screen, self.frame_color, cell_rect, self.frame_width)
                self.cells[i_row][i_col].draw(cell_rect)

