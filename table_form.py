import wx
import wx.grid

from my_table import MyModel


class MyFrame(wx.Frame):
    def __init__(self, parent, table_name, file_path):
        wx.Frame.__init__(self, parent, title=table_name, size=(720,405))
        self.model = MyModel(table_name, file_path)
        self.table = wx.grid.Grid(self)
        self.table.SetTable(self.model)

        self.add_row_button = wx.Button(self, label="Добавить строку")
        self.add_row_button.Bind(wx.EVT_BUTTON, self.on_add_row)
        self.add_col_button = wx.Button(self, label="Добавить столбец")
        self.add_col_button.Bind(wx.EVT_BUTTON, self.on_add_col)
        self.delete_row_button = wx.Button(self, label="Удалить строку")
        self.delete_row_button.Bind(wx.EVT_BUTTON, self.on_delete_row)
        self.delete_col_button = wx.Button(self, label="Удалить столбец")
        self.delete_col_button.Bind(wx.EVT_BUTTON, self.on_delete_col)

        self.save_button = wx.Button(self, label="Сохранить")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer.Add(self.add_row_button, 0, wx.ALL, 5)
        self.button_sizer.Add(self.add_col_button, 0, wx.ALL, 5)
        self.button_sizer.Add(self.delete_row_button, 0, wx.ALL, 5)
        self.button_sizer.Add(self.delete_col_button, 0, wx.ALL, 5)
        self.button_sizer.Add(self.save_button, 0, wx.ALL, 5)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.table, 1, wx.EXPAND)
        self.sizer.Add(self.button_sizer, 0, wx.ALIGN_CENTER)

        self.SetSizer(self.sizer)

    def on_add_row(self, event):
        print("Добавление строки")
        if self.model.AppendRows():
            print("Модель обновлена:", self.model.data)
            msg = wx.grid.GridTableMessage(
                self.model,
                wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED,
                1
            )
            self.table.ProcessTableMessage(msg)
    def on_add_col(self, event):
        print("Добавление столбца")
        if self.model.AppendCols():
            print("Модель обновлена:", self.model.data)
            msg = wx.grid.GridTableMessage(
                self.model,
                wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED,
                1
            )
            self.table.ProcessTableMessage(msg)

    def on_delete_row(self, event):
        print("Удаление строки")
        row = max(0, self.table.GetGridCursorRow())
        if self.model.DeleteRows(row):
            print("Модель обновлена:", self.model.data)
            msg = wx.grid.GridTableMessage(
                self.model,
                wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,
                row,
                1
            )
            self.table.ProcessTableMessage(msg)

    def on_delete_col(self, event):
        print("Удаление столбца")
        col = max(0, self.table.GetGridCursorCol())
        if col < len(self.model.data[0]) - 1:
            if self.model.DeleteCols(col):
                print("Модель обновлена:", self.model.data)
                msg = wx.grid.GridTableMessage(
                    self.model,
                    wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED,
                    col,
                    1
                )
                self.table.ProcessTableMessage(msg)

    def on_save(self, event):
        print("Сохранение данных в файл")
        self.model.save_data()