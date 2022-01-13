import wx
import wx.adv

from .ui import AboutDialog
from ..static import *


class WFAboutDialog(AboutDialog):
    def __init__(self, parent, icon):
        super().__init__(parent)
        self.icon_app.SetIcon(icon)
        self.text_name_version.SetLabel(f'{ST_NAME} {ST_VERSION}')
        self.text_desc.SetLabel(ST_DESCRIPTION)
        self.text_using.SetLabel(f'using wxPython-{wx.VERSION_STRING}-'
                                 f'{wx.PlatformInformation().GetOperatingSystemFamilyName()}')
        self.link_copyright.SetURL(ST_LICENSE_LINK)
        self.link_copyright.SetLabel(ST_COPYRIGHT)
        lic = wx.TextCtrl(self.pane_lic, value=ST_LICENSE,
                          style=wx.TE_BESTWRAP | wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP)
        self.sizer_license.Add(lic, 1, wx.EXPAND, 5)
        self.pane_lic.Layout()
        self.sizer_license.Fit(self.pane_lic)

    def on_license_collapse(self, event):
        self.Layout()

    def add_link(self, label, url):
        link = wx.adv.HyperlinkCtrl(self, label=label, url=url)
        self.sizer_desc.Add(link, 0, wx.ALL, 5)
