import wx

from . import ui


if __name__ == '__main__':
    app = wx.App(False)
    frame = ui.WFMainFrame()
    frame.Show(True)
    app.MainLoop()
