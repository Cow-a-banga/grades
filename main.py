import wx
import wx.grid
import pickle

from rating_form import RatingWindow
from table_form import MyFrame


class StartFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Стартовое окно")


        self.menu_bar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.open_item = self.file_menu.Append(wx.ID_OPEN, "Открыть", "Открыть файл с данными")
        self.new_item = self.file_menu.Append(wx.ID_NEW, "Новый", "Создать новый файл с данными")
        self.menu_bar.Append(self.file_menu, "Файл")
        self.SetMenuBar(self.menu_bar)

        self.Bind(wx.EVT_MENU, self.on_open, self.open_item)
        self.Bind(wx.EVT_MENU, self.on_new, self.new_item)

        self.modules_button = wx.Button(self, label="Модули")
        self.modules_button.Bind(wx.EVT_BUTTON, self.on_modules)
        self.rating_button = wx.Button(self, label="Рейтинг")
        self.rating_button.Bind(wx.EVT_BUTTON, self.on_rating)

        self.modules_button.Disable()
        self.rating_button.Disable()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.modules_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.rating_button, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.sizer)

    def on_open(self, event):
        dialog = wx.FileDialog(self, "Выберите файл с данными", "", "", "Pickle files (*.pkl)|*.pkl",
                               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            print(f"Выбран файл: {path}")
            self.file_path = path
            self.modules_button.Enable()
            self.rating_button.Enable()

    def on_new(self, event):
        dialog = wx.FileDialog(self, "Создайте новый файл с данными", "", "", "Pickle files (*.pkl)|*.pkl",
                               wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            print(f"Создан файл: {path}")
            self.file_path = path
            tables = {}
            with open(path, "wb") as file:
                pickle.dump(tables, file)
            self.modules_button.Enable()
            self.rating_button.Enable()

    def on_modules(self, event):
        modules_frame = ModulesFrame(self)
        modules_frame.Show()


    def on_students(self, event):
        pass

    def on_rating(self, event):
        with open(self.file_path, "rb") as file:
            ratings = {}
            tables = pickle.load(file)
        for module in tables:
            module_rating = [[arr[0], arr[-1]] for arr in tables[module][0]]
            for person_rating in module_rating:
                if person_rating[0] in ratings:
                    ratings[person_rating[0]].append(person_rating[1])
                else:
                    ratings[person_rating[0]] = [person_rating[1]]
        for name in ratings:
            ratings[name] = sum(ratings[name])/len(ratings[name])
        rating_list = [[name, score] for name, score in ratings.items()]
        rating_list.sort(key=lambda x: x[1], reverse=True)

        rating_frame = RatingWindow(self, rating_list)
        rating_frame.Show()



class ModulesFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Список модулей")
        self.parent = parent

        self.modules_list = wx.ListBox(self)
        self.modules_list.Bind(wx.EVT_LISTBOX_DCLICK, self.on_select)

        self.load_modules()

        self.add_button = wx.Button(self, label="Добавить модуль")
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add)
        self.delete_button = wx.Button(self, label="Удалить модуль")
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_delete)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.modules_list, 1, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.add_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.delete_button, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.sizer)

    def load_modules(self):
        try:
            with open(self.parent.file_path, "rb") as file:
                tables = pickle.load(file)
                modules = list(tables.keys())
                print(f"Загружены модули: {modules}")
                self.modules_list.Set(modules)
        except FileNotFoundError:
            print("Файл с данными не найден")

    def save_modules(self):
        try:
            with open(self.parent.file_path, "rb") as file:
                tables = pickle.load(file)
            modules = self.modules_list.GetItems()
            print(f"Сохранены модули: {modules}")
            for module in modules:
                if module not in tables:
                    tables[module] = ([["", 0]], ["Имя", "Среднее"])
            for module in list(tables.keys()):
                if module not in modules:
                    tables.pop(module)
            with open(self.parent.file_path, "wb") as file:
                pickle.dump(tables, file)
        except FileNotFoundError:
            print("Файл с данными не найден")

    def on_select(self, event):
        module = event.GetString()
        table_frame = MyFrame(self, module, self.parent.file_path)
        table_frame.Show()

    def on_add(self, event):
        name = wx.GetTextFromUser("Введите имя модуля:", "Новый модуль")
        if name:
            self.modules_list.Append(name)
            self.save_modules()

    def on_delete(self, event):
        selection = self.modules_list.GetSelection()
        if selection != wx.NOT_FOUND:
            name = self.modules_list.GetString(selection)
            if wx.MessageBox(f"Вы уверены, что хотите удалить модуль {name}?", "Подтверждение",
                             wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                self.modules_list.Delete(selection)
                self.save_modules()

if __name__ == "__main__":
    app = wx.App()
    frame = StartFrame(None)
    frame.Show()
    app.MainLoop()
