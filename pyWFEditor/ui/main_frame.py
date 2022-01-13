import io
import os
import pprint

import wx
import wx.adv
import wx.lib.imagebrowser

from . import about_dialog, ui, wfp
from .. import static, utils, watchface


class WFMainFrame(ui.MainFrame):
    def __init__(self):
        super().__init__(None)
        # self.SetMinSize(())
        self.logger = utils.Logging(f'{static.ST_PKG_NAME}.log')

        self.filehistory = wx.FileHistory(5)
        self.filehistory.UseMenu(self.menu_file)
        self.Bind(wx.EVT_MENU_RANGE, self.on_file_history, id=wx.ID_FILE1, id2=wx.ID_FILE9)

        self.icon_app = wx.Icon(static.APP_ICON)
        self.SetIcon(self.icon_app)

        self.curr_dir = os.getcwd()
        self.curr_file = None
        self.items_images = {}

        self.panel_preview = wx.lib.imagebrowser.ImageView(self, size=(200, -1))
        self.sizer_main.Add(self.panel_preview, (0, 0), (1, 1), wx.EXPAND, 5)
        self.Layout()

        self.list_images = wx.adv.EditableListBox(self.page_img_list, label='Images list', size=(200, -1),
                                                  style=wx.adv.EL_ALLOW_NEW | wx.adv.EL_ALLOW_DELETE)
        self.list_images.GetNewButton().Bind(wx.EVT_BUTTON, self.on_btn_img_add)
        self.sizer_img_list.Add(self.list_images, 1, wx.LEFT | wx.BOTTOM | wx.EXPAND, 1)
        self.panel_img_list_view = wx.lib.imagebrowser.ImageView(self.page_img_list)
        self.panel_img_list_view.SetSizeHints((200, 200), (200, 200))
        self.sizer_img_list.Add(self.panel_img_list_view, 1, wx.ALL | wx.EXPAND, 5)

        self.cat_background = wfp.WFPBackground(self.page_options)
        self.cat_time = wfp.WFPTime(self.page_options)
        self.cat_date = None
        self.cat_days_progress = None
        self.cat_steps_progress = None
        self.cat_activity = None
        self.cat_status = None
        self.cat_battery = None
        self.cat_analog_clock = None
        self.cat_weather = None
        self.cat_shortcuts = None
        self.cat_animation = None

        self.cat_ids = {
            2: self.cat_background,
            3: self.cat_time,
            4: self.cat_date,
            5: self.cat_days_progress,
            6: self.cat_steps_progress,
            7: self.cat_activity,
            8: self.cat_status,
            9: self.cat_battery,
            10: self.cat_analog_clock,
            11: self.cat_weather,
            12: self.cat_shortcuts,
            13: self.cat_animation,
        }

        self.list_images.Bind(wx.EVT_LIST_INSERT_ITEM, self.on_list_insert)
        self.list_images.Bind(wx.EVT_LIST_DELETE_ITEM, self.on_list_del)
        self.list_images.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_list_order)

        wx.LogMessage('The program is running')

    def on_close(self, event):
        wx.LogMessage('Exiting...')
        event.Skip()

    def on_quit(self, event):
        self.Close()

    def on_about(self, event):
        about = about_dialog.WFAboutDialog(self, self.icon_app)
        about.add_link('Homepage: GitHub', static.ST_HOMEPAGE)
        about.ShowModal()
        about.Destroy()

    def on_file_history(self, evt: wx.Event):
        n = evt.GetId() - wx.ID_FILE1
        print(f'on_file_history n {n}')
        self.curr_file = self.filehistory.GetHistoryFile(n)
        print(f'on_file_history path {self.curr_file}')
        self.filehistory.AddFileToHistory(self.curr_file)

        self._wf_open()

    def on_list_insert(self, evt: wx.ListEvent):
        txt = evt.GetText()
        if txt == '':
            return
        self.items_images[txt] = evt.GetIndex()

    def on_list_del(self, evt: wx.ListEvent):
        self.items_images.pop(evt.GetText(), None)

    def on_list_order(self, evt: wx.ListEvent):
        itm = evt.GetText()
        idx_new = evt.GetIndex()
        idx_old = self.items_images.get(itm, idx_new)
        diff = idx_new - idx_old
        if not diff:
            return
        self.items_images[itm] = idx_new
        self.items_images[self.list_images.GetListCtrl().GetItemText(idx_new - diff)] = idx_old

    def on_btn_img_add(self, event):
        dlg = wx.FileDialog(
            self,
            'Open Images',
            wildcard=utils.WC_IMAGES,
            style=wx.FD_OPEN | wx.FD_MULTIPLE
        )
        if dlg.ShowModal() == wx.ID_CANCEL:
            return

        old_s = dict.fromkeys(self.list_images.GetStrings())
        old_s.update(dict.fromkeys(dlg.GetPaths()))
        self.list_images.SetStrings(list(old_s))

    def wf_create(self, event: wx.Event):
        event.Skip()
        self._state_change(True)

    def wf_open(self, event):
        open_file_dlg = wx.FileDialog(
            self,
            'Open Watchface file',
            self.curr_dir,
            wx.EmptyString,
            wx.EmptyString,
            wx.FD_OPEN# | wx.FD_CHANGE_DIR
        )
        if open_file_dlg.ShowModal() == wx.ID_CANCEL:
            return

        self.curr_dir = open_file_dlg.GetDirectory()
        self.curr_file = open_file_dlg.GetPath()
        self.filehistory.AddFileToHistory(self.curr_file)
        open_file_dlg.Destroy()

        self._wf_open()

    def wf_save(self, event):
        event.Skip()

    def wf_saveas(self, event):
        event.Skip()

    def wf_close(self, event):
        event.Skip()
        self.sizer_main.Clear(True)
        self.curr_file = None
        self._state_change(False)

    def redraw(self, event):
        # dc = wx.WindowDC(self)
        # dc = wx.PaintDC(self)
        # for bm in [wx.Bitmap(wx.Image(static.PREV_TEST)), wx.Bitmap(wx.Image(static.PREV_TEST_8))]:
        #     dc.DrawBitmap(bm, 0, 0, useMask=True)
        self.panel_preview.SetValue(static.PREV_TEST)
        # self.panel_preview.DrawImage(dc)
        # dc.DrawBitmap(wx.Bitmap(wx.Image(static.PREV_TEST)), 0, 0, useMask=True)
        # dc.DrawBitmap(wx.Bitmap(wx.Image(static.PREV_TEST_8)), 0, 20, useMask=True)

    def _wf_open(self):
        try:
            wf = watchface.WatchFace.from_file(self.curr_file)
        except watchface.errors.WFError as e:
            wx.LogError(e.message)
            self.curr_file = None
            return
        x = io.StringIO()
        x.write('Parameters:\n')
        pprint.pprint(wf.params, width=3, stream=x)
        wx.LogDebug(x.getvalue())

        # TODO

        self.Layout()
        self._state_change(True)
        wx.LogMessage(f'File {self.curr_file} opened')

    def _state_change(self, enable: bool):
        self.item_menu_file_save.Enable(enable)
        self.item_menu_file_saveas.Enable(enable)
        self.item_menu_file_close.Enable(enable)
