import wx
import wx.grid
import pickle

from rating_form import RatingWindow
from table_form import MyFrame


class StartFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Стартовое окно")

        # Создать меню
        self.menu_bar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.open_item = self.file_menu.Append(wx.ID_OPEN, "Открыть", "Открыть файл с данными")
        self.new_item = self.file_menu.Append(wx.ID_NEW, "Новый", "Создать новый файл с данными")
        self.menu_bar.Append(self.file_menu, "Файл")
        self.SetMenuBar(self.menu_bar)

        # Привязать события к пунктам меню
        self.Bind(wx.EVT_MENU, self.on_open, self.open_item)
        self.Bind(wx.EVT_MENU, self.on_new, self.new_item)

        # Создать кнопки
        self.modules_button = wx.Button(self, label="Модули")
        self.modules_button.Bind(wx.EVT_BUTTON, self.on_modules)
        # self.students_button = wx.Button(self, label="Ученики")
        # self.students_button.Bind(wx.EVT_BUTTON, self.on_students)
        self.rating_button = wx.Button(self, label="Рейтинг")
        self.rating_button.Bind(wx.EVT_BUTTON, self.on_rating)

        # Сделать кнопки недоступными до выбора файла
        self.modules_button.Disable()
        # self.students_button.Disable()
        self.rating_button.Disable()

        # Расположить кнопки в столбец
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.modules_button, 0, wx.ALL | wx.EXPAND, 5)
        # self.sizer.Add(self.students_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.rating_button, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.sizer)

    def on_open(self, event):
        # Открыть диалог выбора файла
        dialog = wx.FileDialog(self, "Выберите файл с данными", "", "", "Pickle files (*.pkl)|*.pkl",
                               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            # Получить путь к выбранному файлу
            path = dialog.GetPath()
            print(f"Выбран файл: {path}")
            # Сохранить путь к файлу в атрибуте класса
            self.file_path = path
            # Активировать кнопки
            self.modules_button.Enable()
            # self.students_button.Enable()
            self.rating_button.Enable()

    def on_new(self, event):
        # Открыть диалог создания файла
        dialog = wx.FileDialog(self, "Создайте новый файл с данными", "", "", "Pickle files (*.pkl)|*.pkl",
                               wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            # Получить путь к созданному файлу
            path = dialog.GetPath()
            print(f"Создан файл: {path}")
            # Сохранить путь к файлу в атрибуте класса
            self.file_path = path
            # Создать пустой словарь с данными таблиц и записать его в файл
            tables = {}
            with open(path, "wb") as file:
                pickle.dump(tables, file)
            # Активировать кнопки
            self.modules_button.Enable()
            # self.students_button.Enable()
            self.rating_button.Enable()

    def on_modules(self, event):
        # Открыть окно со списком модулей
        modules_frame = ModulesFrame(self)
        modules_frame.Show()


    def on_students(self, event):
        # Открыть окно со списком учеников (не реализовано)
        pass

    def on_rating(self, event):
        # Открыть окно с рейтингом учеников (не реализовано)
        with open(self.file_path, "rb") as file:
            ratings = {}
            tables = pickle.load(file)  # Словарь с данными таблиц
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
        self.parent = parent  # Ссылка на родительское окно

        # Создать список модулей
        self.modules_list = wx.ListBox(self)
        self.modules_list.Bind(wx.EVT_LISTBOX_DCLICK, self.on_select)

        # Загрузить имена модулей из файла
        self.load_modules()

        # Создать кнопки для добавления и удаления модулей
        self.add_button = wx.Button(self, label="Добавить модуль")
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add)
        self.delete_button = wx.Button(self, label="Удалить модуль")
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_delete)

        # Расположить список и кнопки в столбец
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.modules_list, 1, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.add_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.delete_button, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.sizer)

    def load_modules(self):
        # Загрузить имена модулей из файла
        try:
            with open(self.parent.file_path, "rb") as file:
                tables = pickle.load(file)  # Словарь с данными таблиц
                modules = list(tables.keys())  # Список имен модулей
                print(f"Загружены модули: {modules}")
                # Отобразить имена модулей в списке
                self.modules_list.Set(modules)
        except FileNotFoundError:
            print("Файл с данными не найден")

    def save_modules(self):
        # Сохранить имена модулей в файл
        try:
            with open(self.parent.file_path, "rb") as file:
                tables = pickle.load(file)  # Словарь с данными таблиц
            modules = self.modules_list.GetItems()  # Список имен модулей
            print(f"Сохранены модули: {modules}")
            # Обновить словарь с данными таблиц по именам модулей
            for module in modules:
                if module not in tables:  # Если нет данных для этого модуля
                    tables[module] = ([["", 0]], ["Имя", "Среднее"])  # Добавить данные по умолчанию
            for module in list(tables.keys()):
                if module not in modules:  # Если есть лишние данные для удаленного модуля
                    tables.pop(module)  # Удалить данные
            with open(self.parent.file_path, "wb") as file:
                pickle.dump(tables, file)  # Записать словарь в файл
        except FileNotFoundError:
            print("Файл с данными не найден")

    def on_select(self, event):
        # Открыть окно с таблицей по имени модуля
        module = event.GetString()  # Получить имя модуля из события
        table_frame = MyFrame(self, module, self.parent.file_path)  # Создать окно с таблицей по имени модуля
        table_frame.Show()

    def on_add(self, event):
        # Добавить новый модуль в список
        name = wx.GetTextFromUser("Введите имя модуля:", "Новый модуль")
        if name:
            self.modules_list.Append(name)  # Добавить имя в список
            self.save_modules()  # Сохранить имена в файл

    def on_delete(self, event):
        # Удалить выбранный модуль из списка
        selection = self.modules_list.GetSelection()  # Получить индекс выбранного элемента
        if selection != wx.NOT_FOUND:  # Если есть выбранный элемент
            name = self.modules_list.GetString(selection)  # Получить имя выбранного элемента
            if wx.MessageBox(f"Вы уверены, что хотите удалить модуль {name}?", "Подтверждение",
                             wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                # Если пользователь подтвердил удаление
                self.modules_list.Delete(selection)  # Удалить элемент из списка
                self.save_modules()  # Сохранить имена в файл

if __name__ == "__main__":
    app = wx.App()
    frame = StartFrame(None)
    frame.Show()
    app.MainLoop()
