import os

import wx
import wx.adv
import wx.lib.imagebrowser

from ..ui import ImgSelectDialog


class WFProperty(wx.StaticBoxSizer):
    def __init__(self, parent: wx.Window, label, orient=wx.HORIZONTAL, psz=None):
        p = parent.GetStaticBox() if isinstance(parent, wx.StaticBoxSizer) else parent
        psz = psz or (parent if isinstance(parent, wx.StaticBoxSizer) else parent.GetSizer())
        super().__init__(orient, p, label=label)
        self.sbox = self.GetStaticBox()

        psz.Add(self, 0, wx.BOTTOM | wx.LEFT | wx.RIGHT, 5)
        p.Layout()


class WFPImageListCtrl(wx.ListCtrl):
    def __init__(self, parent, multiple_select=False):
        super().__init__(parent, style=wx.LC_NO_HEADER | wx.LC_REPORT | (0 if multiple_select else wx.LC_SINGLE_SEL) | wx.LC_VIRTUAL)

        # self.SetMinSize((200, -1))
        self.EnableCheckBoxes(multiple_select)

        while not hasattr(parent, 'items_images'):
            # find WFMainFrame
            parent = parent.GetParent()
        self.images = parent.items_images
        self.checked = set()

        self.fill_list()

        self.Layout()
        self.SetMinSize(self.GetBestSize())
        self.Bind(wx.EVT_LIST_ITEM_CHECKED, self.on_item_checked)
        self.Bind(wx.EVT_LIST_ITEM_UNCHECKED, self.on_item_unchecked)

    def on_item_checked(self, evt: wx.ListEvent):
        self.checked.add(evt.GetIndex())

    def on_item_unchecked(self, evt: wx.ListEvent):
        self.checked.discard(evt.GetIndex())

    def OnGetItemText(self, item, col):
        for name, idx in self.images.items():
            if idx == item:
                # return os.path.basename(name)
                return name

    def OnGetItemIsChecked(self, item):
        return item in self.checked

    def fill_list(self):
        self.InsertColumn(0, 'name')
        self.SetItemCount(len(self.images))
        for name, idx in self.images.items():
            self.SetItem(idx, 0, name)
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)

    def get_selected(self):
        result = []
        if self.HasCheckBoxes():
            result += sorted(self.checked)
        else:
            x = self.GetFirstSelected()
            if x != -1:
                result.append(x)
        return result


class WFPImgSelectDialog(ImgSelectDialog):
    def __init__(self, parent, selected, multiple_select=False):
        super().__init__(parent)

        self.list_img_list = WFPImageListCtrl(self, multiple_select)
        if self.list_img_list.HasCheckBoxes():
            for name in selected:
                i = self.list_img_list.images.get(name)
                if i is not None:
                    self.list_img_list.CheckItem(i, True)
        elif selected:
            i = self.list_img_list.images.get(selected[0])
            if i is not None:
                self.list_img_list.Select(i, True)
        self.sizer_main.Add(self.list_img_list, (0, 0), (2, 1), wx.ALL | wx.EXPAND, 5)

        self.view_panel = wx.lib.imagebrowser.ImageView(self)
        self.view_panel.SetSizeHints((200, 200), (200, 200))
        self.sizer_main.Add(self.view_panel, (0, 1), (1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)

        self.sizer_btnsNo.SetLabel('Clear')

        self.Layout()
        self.SetMinSize(self.GetBestSize())
        self.Centre(wx.BOTH)

    def on_clear_selected(self, evt):
        if self.list_img_list.HasCheckBoxes():
            for i in self.list_img_list.get_selected():
                self.list_img_list.CheckItem(i, False)
        else:
            for i in self.list_img_list.get_selected():
                self.list_img_list.Select(i, False)

    def get_selected(self):
        return (name for i in self.list_img_list.get_selected()
                for name, idx in self.list_img_list.images.items()
                if i == idx)


class WFPImage(WFProperty):
    def __init__(self, parent: wx.Window, psz=None, multiple_select=False):
        super().__init__(parent, 'Image', psz=psz)
        self.multiple_select = multiple_select
        self.selected = []

        self.position = WFPPosition(self.sbox, psz=self)

        sz_sel = wx.BoxSizer(wx.VERTICAL)

        self.btn_select = wx.Button(self.sbox, label='Select...')
        sz_sel.Add(self.btn_select, 0, wx.LEFT | wx.RIGHT, 5)
        self.sbox.Bind(wx.EVT_BUTTON, self.on_btn_select)

        # TODO: how to dynamically update???
        self.txt_selected = wx.StaticText(self.sbox, label=('[0]'  if multiple_select else 'None'))
        sz_sel.Add(self.txt_selected, 0, wx.LEFT | wx.RIGHT, 5)

        self.Add(sz_sel, 1, wx.EXPAND)

    def on_btn_select(self, evt):
        dlg = WFPImgSelectDialog(self.sbox, self.selected, self.multiple_select)

        if dlg.ShowModal() == wx.ID_OK:
            self.set_selected(dlg.get_selected(), dlg.list_img_list.images)

    def set_selected(self, sel_names, images):
        self.selected.clear()
        for sel_name in sel_names:
            if sel_name in images:
                self.selected.append(sel_name)
        if self.multiple_select:
            label = f'[{len(self.selected)}]'
        else:
            label = os.path.basename(self.selected[0]) if self.selected else 'None'
        self.txt_selected.SetLabel(label)


class WFPImageSet(WFPImage):
    def __init__(self, parent: wx.Window, label='Image Set', psz=None):
        super().__init__(parent, psz, True)
        self.sbox.SetLabel(label)


class WFPPosition(WFProperty):
    def __init__(self, parent: wx.Window, label='position', x=0, y=0, psz=None):
        super().__init__(parent, label, psz=psz)

        stext_x = wx.StaticText(self.sbox, label='X:')
        self.Add(stext_x, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.LEFT, 5)
        self.spinc_x = wx.SpinCtrl(self.sbox, min=-1000, max=1000, initial=x)  # size=(110, -1),
        self.Add(self.spinc_x, 0, wx.BOTTOM | wx.RIGHT, 5)

        stext_y = wx.StaticText(self.sbox, label='Y:')
        self.Add(stext_y, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, 5)
        self.spinc_y = wx.SpinCtrl(self.sbox, min=-1000, max=1000, initial=y)  # size=(110, -1),
        self.Add(self.spinc_y, 0, wx.BOTTOM | wx.RIGHT, 5)


class WFPNumber(wx.StaticBoxSizer):
    def __init__(self): pass
