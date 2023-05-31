import wx
import wx.grid
import pickle


class MyModel(wx.grid.GridTableBase):
    def __init__(self, table_name, file_path):
        wx.grid.GridTableBase.__init__(self)
        self.table_name = table_name  # Имя таблицы
        self.file_path = file_path  # Имя таблицы
        self.data = []  # Пустой список для данных
        self.col_names = []  # Список для названий столбцов
        self.load_data()  # Загрузить данные из файла

    def get_average(self, row):
        segment = row[1:-1]
        return 0 if len(segment) == 0 else sum(segment) / len(segment)

    def update_average(self):
        # Добавить столбец среднего значения для каждой строки
        for row in self.data:
            row[-1] = self.get_average(row)

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data[0]) if self.data else 0

    def GetValue(self, row, col):
        return self.data[row][col]

    def SetValue(self, row, col, value):
        # Изменить значение ячейки и обновить среднее
        if col == 0:  # Если это столбец с именем
            self.data[row][col] = value  # Просто изменить значение
        else:  # Если это столбец с оценкой
            try:
                value = int(value)
                if 0 <= value <= 5:
                    self.data[row][col] = value
                    self.data[row][-1] = self.get_average(self.data[row])
                else:
                    raise ValueError("Значение должно быть от 0 до 5")
            except ValueError as e:
                wx.MessageBox(str(e), "Ошибка")

    def GetColLabelValue(self, col):
        return self.col_names[col]

    def AppendRows(self, numRows=1):
        # Добавить новую строку с нулевыми значениями и обновить среднее
        for i in range(numRows):
            self.data.append([""] + [0] * (len(self.col_names) - 1))
            self.update_average()
        return True

    def AppendCols(self, numCols=1):
        # Добавить новый столбец с нулевыми значениями и запрашивать имя столбца
        for i in range(numCols):
            name = wx.GetTextFromUser("Введите имя столбца:", "Новый столбец")
            if name:
                self.col_names.insert(-1, name)  # Добавить имя в список названий
                for row in self.data:
                    row.insert(-1, 0)  # Добавить нулевое значение в каждую строку
                    row[-1] = self.get_average(row)
            else:
                return False
        return True

    def DeleteRows(self, pos=0, numRows=1):
        # Удалить строку и обновить среднее
        for i in range(numRows):
            if pos < len(self.data):
                self.data.pop(pos)
            else:
                return False
        return True

    def DeleteCols(self, pos=0, numCols=1):
        # Удалить столбец и обновить среднее
        for i in range(numCols):
            if pos < len(self.col_names) - 2:  # Не удалять столбец с именем или средним
                self.col_names.pop(pos + 1)  # Сдвинуть индекс на один из-за столбца с именем
                for row in self.data:
                    row.pop(pos + 1)  # Сдвинуть индекс на один из-за столбца с именем
                    row[-1] = sum(row[1:-1]) / len(row[1:-1])
            else:
                return False
        return True

    def load_data(self):
        # Загрузить данные из файла по имени таблицы
        try:
            with open(self.file_path, "rb") as file:
                tables = pickle.load(file)  # Словарь с данными таблиц
                if self.table_name in tables:  # Если есть данные для этой таблицы
                    table = tables[self.table_name]  # Кортеж из двух списков: данных и названий столбцов
                    self.data = table[0]  # Загрузить данные в модель
                    self.col_names = table[1]  # Загрузить названия в модель
                    print(f"Данные для таблицы {self.table_name} загружены из файла")
                else:
                    self.data = [[""]]
                    self.col_names = ["Имя", "Среднее"]
        except FileNotFoundError:
            print("Файл с данными не найден")

    def save_data(self):
        # Сохранить данные в файл по имени таблицы
        try:
            with open(self.file_path, "rb") as file:
                tables = pickle.load(file)  # Словарь с данными таблиц
        except FileNotFoundError:
            tables = {}  # Создать новый словарь, если файл не найден
        table = (self.data, self.col_names)  # Кортеж из двух списков: данных и названий столбцов
        tables[self.table_name] = table  # Сохранить данные для этой таблицы
        with open(self.file_path, "wb") as file:
            pickle.dump(tables, file)  # Записать словарь в файл
        print(f"Данные для таблицы {self.table_name} сохранены в файл")
