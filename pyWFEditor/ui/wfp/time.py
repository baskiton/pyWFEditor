import wx

from . import basics


class WFPTwoDigits(wx.Panel):
    def __init__(self, parent: wx.Notebook, label, visible=False):
        super().__init__(parent, style=wx.TAB_TRAVERSAL)
        sz = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sz)

        self.visible = wx.CheckBox(self, label='Visible')
        self.visible.SetValue(visible)
        self.visible.Bind(wx.EVT_CHECKBOX, self.on_visible)
        sz.Add(self.visible, 0, 0)

        self.tens = basics.WFPImageSet(self, 'Tens')    # (1)
        self.ones = basics.WFPImageSet(self, 'Ones')    # (2)

        self.on_visible()
        sz.Fit(self)
        parent.AddPage(self, label)

    def on_visible(self, evt=None):
        self.tens.sbox.Enable(self.visible.GetValue())
        self.ones.sbox.Enable(self.visible.GetValue())
        self.Layout()
