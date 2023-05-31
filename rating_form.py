import wx
import wx.grid


class RatingWindow(wx.Frame):
    def __init__(self, parent, data):
        wx.Frame.__init__(self, parent, title="Рейтинг")
        panel = wx.ScrolledWindow(self)
        list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT)

        list_ctrl.InsertColumn(0, "Имя")
        list_ctrl.InsertColumn(1, "Рейтинг")

        for i, row in enumerate(data):
            list_ctrl.InsertItem(i, row[0])
            list_ctrl.SetItem(i, 1, str(row[1]))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(list_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        panel.SetSizer(sizer)

        panel.SetScrollRate(10, 10)
        panel.SetMinSize((300, 200))
