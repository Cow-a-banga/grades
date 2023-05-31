import wx
import wx.grid
import pickle


class MyModel(wx.grid.GridTableBase):
    def __init__(self, table_name, file_path):
        wx.grid.GridTableBase.__init__(self)
        self.table_name = table_name
        self.file_path = file_path
        self.data = []
        self.col_names = []
        self.load_data()

    def get_average(self, row):
        segment = row[1:-1]
        return 0 if len(segment) == 0 else sum(segment) / len(segment)

    def update_average(self):
        for row in self.data:
            row[-1] = self.get_average(row)

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data[0]) if self.data else 0

    def GetValue(self, row, col):
        return self.data[row][col]

    def SetValue(self, row, col, value):
        if col == 0:
            self.data[row][col] = value
        else:
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
        for i in range(numRows):
            self.data.append([""] + [0] * (len(self.col_names) - 1))
            self.update_average()
        return True

    def AppendCols(self, numCols=1):
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
        for i in range(numRows):
            if pos < len(self.data):
                self.data.pop(pos)
            else:
                return False
        return True

    def DeleteCols(self, pos=0, numCols=1):
        for i in range(numCols):
            if pos < len(self.col_names) - 2:
                self.col_names.pop(pos + 1)
                for row in self.data:
                    row.pop(pos + 1)
                    row[-1] = sum(row[1:-1]) / len(row[1:-1])
            else:
                return False
        return True

    def load_data(self):
        try:
            with open(self.file_path, "rb") as file:
                tables = pickle.load(file)
                if self.table_name in tables:
                    table = tables[self.table_name]
                    self.data = table[0]
                    self.col_names = table[1]
                    print(f"Данные для таблицы {self.table_name} загружены из файла")
                else:
                    self.data = [[""]]
                    self.col_names = ["Имя", "Среднее"]
        except FileNotFoundError:
            print("Файл с данными не найден")

    def save_data(self):
        try:
            with open(self.file_path, "rb") as file:
                tables = pickle.load(file)
        except FileNotFoundError:
            tables = {}
        table = (self.data, self.col_names)
        tables[self.table_name] = table
        with open(self.file_path, "wb") as file:
            pickle.dump(tables, file)
        print(f"Данные для таблицы {self.table_name} сохранены в файл")
