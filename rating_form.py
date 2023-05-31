import wx
import wx.grid


class RatingWindow(wx.Frame):
    def __init__(self, parent, data):
        wx.Frame.__init__(self, parent, title="Рейтинг")
        panel = wx.ScrolledWindow(self)
        list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT)

        list_ctrl.InsertColumn(0, "Имя")
        list_ctrl.InsertColumn(1, "Рейтинг")
        list_ctrl.InsertColumn(2, "Двоек")
        list_ctrl.InsertColumn(3, "Допуск к экзамену")

        for i, row in enumerate(data):
            list_ctrl.InsertItem(i, row[0])
            list_ctrl.SetItem(i, 1, str(row[1]))
            list_ctrl.SetItem(i, 2, str(row[2]))
            list_ctrl.SetItem(i, 3, "Допущен" if row[2] == 0 else "Не допущен")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(list_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        panel.SetSizer(sizer)

        panel.SetScrollRate(10, 10)
        panel.SetMinSize((300, 200))
