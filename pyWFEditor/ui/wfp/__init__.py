import wx

from . import basics, time


class WFPCategory(wx.CollapsiblePane):
    def __init__(self, parent: wx.Window, label: str, with_enabling=True, enabled=False):
        super().__init__(parent, label=label, style=wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE)
        # self.Collapse(False)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.children_elements = []

        if with_enabling:
            self.chbox_enable = wx.CheckBox(self.pane, label='Enable')
            self.chbox_enable.SetValue(enabled)
            self.chbox_enable.Bind(wx.EVT_CHECKBOX, self.on_enabled)
            self.sizer.Add(self.chbox_enable, 0, 0)
        else:
            class CBDummy:
                def __init__(self, enabled, f):
                    self.v = enabled
                    self.f = f
                def GetValue(self):
                    return self.v
                def SetValue(self, v):
                    self.v = v
                    self.f()
            self.chbox_enable = CBDummy(enabled, self.on_enabled)

        self.sizer_disabled = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer_disabled, 1, wx.EXPAND)

        self.pane.SetSizer(self.sizer)
        self.Layout()
        self.sizer.Fit(self.pane)

        parent.GetSizer().Add(self, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 1)

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_page_collapse)

    @property
    def pane(self) -> wx.Window:
        return self.GetPane()

    def on_page_collapse(self, evt):
        self.on_enabled(evt)
        self.Layout()
        self.GetParent().Layout()

    def on_enabled(self, evt=None):
        is_enabled = self.is_enabled()
        for i in self.children_elements:
            i.Enable(is_enabled)

    def is_enabled(self):
        return self.chbox_enable.GetValue()

    def __bool__(self):
        return self.is_enabled()


class WFPBackground(WFPCategory):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, 'Background', False, True)

        self.bkg = basics.WFPImage(self.pane, self.sizer_disabled)  # (1)
        self.children_elements.append(self.bkg.GetStaticBox())

        # preview WFPImage (2)
        # animations WFPImage (3, 4, 5...)

        # self.sizer.Fit(self)


class WFPTime(WFPCategory):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, 'Time', True, False)

        self.nb = wx.Notebook(self.pane)
        self.children_elements.append(self.nb)
        self.sizer.Add(self.nb, 1, wx.ALL, 5)

        self.hours = time.WFPTwoDigits(self.nb, 'Hours')    # (1)
        self.children_elements.append(self.hours)

        self.minutes = time.WFPTwoDigits(self.nb, 'Minutes')    # (2)
        self.children_elements.append(self.minutes)

        self.seconds = time.WFPTwoDigits(self.nb, 'Seconds')    # (3)
        self.children_elements.append(self.seconds)

        self.am_pm = None   # (4)
        self.delimeter = None   # (5?) draw order?

        self.sunset = None  # (7,8,12)
        self.sunrise = None # (9,10,13)
        # param.get(7)    # SUNSET Number
        # param.get(8)    # SUNSET DELIMETER IMG_IDX
        # param.get(9)    # SUNRISE Number
        # param.get(10)   # SUNRISE DELIMETER IMG_IDX
        # param.get(11)   # 0 ???
        # param.get(12)   # SUNSET NONE Img
        # param.get(13)   # SUNRISE NONE Img
