# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Watch Face Editor", pos = wx.DefaultPosition, size = wx.Size( 640,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 640,500 ), wx.DefaultSize )

        self.menu_bar = wx.MenuBar( 0 )
        self.menu_file = wx.Menu()
        self.item_menu_file_new = wx.MenuItem( self.menu_file, wx.ID_NEW, u"&New", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_file.Append( self.item_menu_file_new )

        self.item_menu_file_open = wx.MenuItem( self.menu_file, wx.ID_OPEN, u"&Open", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_file.Append( self.item_menu_file_open )

        self.item_menu_file_save = wx.MenuItem( self.menu_file, wx.ID_SAVE, u"&Save", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_file.Append( self.item_menu_file_save )
        self.item_menu_file_save.Enable( False )

        self.item_menu_file_saveas = wx.MenuItem( self.menu_file, wx.ID_SAVEAS, u"Save &As...", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_file.Append( self.item_menu_file_saveas )
        self.item_menu_file_saveas.Enable( False )

        self.item_menu_file_close = wx.MenuItem( self.menu_file, wx.ID_CLOSE, u"&Close", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_file.Append( self.item_menu_file_close )
        self.item_menu_file_close.Enable( False )

        self.menu_file.AppendSeparator()

        self.item_menu_file_exit = wx.MenuItem( self.menu_file, wx.ID_EXIT, u"&Quit", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_file.Append( self.item_menu_file_exit )

        self.menu_bar.Append( self.menu_file, u"&File" )

        self.menu_help = wx.Menu()
        self.menu_help.AppendSeparator()

        self.item_menu_help_about = wx.MenuItem( self.menu_help, wx.ID_ABOUT, u"&About", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_help.Append( self.item_menu_help_about )

        self.menu_bar.Append( self.menu_help, u"&Help" )

        self.SetMenuBar( self.menu_bar )

        sizer_main = wx.GridBagSizer( 5, 5 )
        sizer_main.SetFlexibleDirection( wx.BOTH )
        sizer_main.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.pages_opts = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.page_img_list = wx.Panel( self.pages_opts, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer_img_list = wx.BoxSizer( wx.HORIZONTAL )


        self.page_img_list.SetSizer( sizer_img_list )
        self.page_img_list.Layout()
        sizer_img_list.Fit( self.page_img_list )
        self.pages_opts.AddPage( self.page_img_list, u"Images list", True )
        self.page_options = wx.Panel( self.pages_opts, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer_page_collapse = wx.BoxSizer( wx.VERTICAL )


        self.page_options.SetSizer( sizer_page_collapse )
        self.page_options.Layout()
        sizer_page_collapse.Fit( self.page_options )
        self.pages_opts.AddPage( self.page_options, u"Options", False )

        sizer_main.Add( self.pages_opts, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )


        sizer_main.AddGrowableCol( 1 )
        sizer_main.AddGrowableRow( 0 )

        self.SetSizer( sizer_main )
        self.Layout()
        self.status_bar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
        self.sizer_main = sizer_main
        self.sizer_img_list = sizer_img_list

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.on_close )
        self.Bind( wx.EVT_PAINT, self.redraw )
        self.Bind( wx.EVT_MENU, self.wf_create, id = self.item_menu_file_new.GetId() )
        self.Bind( wx.EVT_MENU, self.wf_open, id = self.item_menu_file_open.GetId() )
        self.Bind( wx.EVT_MENU, self.wf_save, id = self.item_menu_file_save.GetId() )
        self.Bind( wx.EVT_MENU, self.wf_saveas, id = self.item_menu_file_saveas.GetId() )
        self.Bind( wx.EVT_MENU, self.wf_close, id = self.item_menu_file_close.GetId() )
        self.Bind( wx.EVT_MENU, self.on_quit, id = self.item_menu_file_exit.GetId() )
        self.Bind( wx.EVT_MENU, self.on_about, id = self.item_menu_help_about.GetId() )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def on_close( self, event ):
        event.Skip()

    def redraw( self, event ):
        event.Skip()

    def wf_create( self, event ):
        event.Skip()

    def wf_open( self, event ):
        event.Skip()

    def wf_save( self, event ):
        event.Skip()

    def wf_saveas( self, event ):
        event.Skip()

    def wf_close( self, event ):
        event.Skip()

    def on_quit( self, event ):
        event.Skip()

    def on_about( self, event ):
        event.Skip()


###########################################################################
## Class AboutDialog
###########################################################################

class AboutDialog ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"About", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        sizer_main = wx.BoxSizer( wx.VERTICAL )

        sizer_up = wx.BoxSizer( wx.HORIZONTAL )

        self.icon_app = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 32,32 ), 0 )
        sizer_up.Add( self.icon_app, 0, wx.ALL, 5 )

        sizer_desc = wx.BoxSizer( wx.VERTICAL )

        sizer_name = wx.BoxSizer( wx.HORIZONTAL )


        sizer_name.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.text_name_version = wx.StaticText( self, wx.ID_ANY, u"%name% %version%", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_name_version.Wrap( -1 )

        self.text_name_version.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        sizer_name.Add( self.text_name_version, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        sizer_name.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        sizer_desc.Add( sizer_name, 1, wx.EXPAND, 5 )

        self.text_desc = wx.StaticText( self, wx.ID_ANY, u"%description%", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_desc.Wrap( -1 )

        sizer_desc.Add( self.text_desc, 0, wx.ALL|wx.EXPAND, 5 )

        self.text_using = wx.StaticText( self, wx.ID_ANY, u"Using %wx%", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_using.Wrap( -1 )

        sizer_desc.Add( self.text_using, 0, wx.ALL|wx.EXPAND, 5 )


        sizer_up.Add( sizer_desc, 1, wx.EXPAND, 5 )


        sizer_main.Add( sizer_up, 0, wx.EXPAND, 5 )

        self.panel_license = wx.CollapsiblePane( self, wx.ID_ANY, u"License", wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE )
        self.panel_license.Collapse( True )

        sizer_license = wx.BoxSizer( wx.VERTICAL )


        self.panel_license.GetPane().SetSizer( sizer_license )
        self.panel_license.GetPane().Layout()
        sizer_license.Fit( self.panel_license.GetPane() )
        sizer_main.Add( self.panel_license, 1, wx.EXPAND |wx.ALL, 5 )

        sizer_low = wx.BoxSizer( wx.HORIZONTAL )

        self.link_copyright = wx.adv.HyperlinkCtrl( self, wx.ID_ANY, u"%label%", u"%url%", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
        sizer_low.Add( self.link_copyright, 1, wx.ALIGN_BOTTOM|wx.ALL, 5 )

        sizer_button = wx.StdDialogButtonSizer()
        self.sizer_buttonOK = wx.Button( self, wx.ID_OK )
        sizer_button.AddButton( self.sizer_buttonOK )
        sizer_button.Realize();

        sizer_low.Add( sizer_button, 0, wx.ALL|wx.EXPAND, 5 )


        sizer_main.Add( sizer_low, 0, wx.EXPAND, 5 )


        self.SetSizer( sizer_main )
        self.Layout()
        sizer_main.Fit( self )
        self.sizer_desc = sizer_desc
        self.sizer_license = sizer_license
        self.pane_lic = self.panel_license.GetPane()

        self.Centre( wx.BOTH )

        # Connect Events
        self.panel_license.Bind( wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_license_collapse )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def on_license_collapse( self, event ):
        event.Skip()


###########################################################################
## Class ImgSelectDialog
###########################################################################

class ImgSelectDialog ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Select Image", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        sizer_main = wx.GridBagSizer( 0, 0 )
        sizer_main.SetFlexibleDirection( wx.BOTH )
        sizer_main.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        sizer_main.SetMinSize( wx.Size( -1,250 ) )
        sizer_btns = wx.StdDialogButtonSizer()
        self.sizer_btnsOK = wx.Button( self, wx.ID_OK )
        sizer_btns.AddButton( self.sizer_btnsOK )
        self.sizer_btnsNo = wx.Button( self, wx.ID_NO )
        sizer_btns.AddButton( self.sizer_btnsNo )
        self.sizer_btnsCancel = wx.Button( self, wx.ID_CANCEL )
        sizer_btns.AddButton( self.sizer_btnsCancel )
        sizer_btns.Realize();

        sizer_main.Add( sizer_btns, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.BOTTOM, 5 )


        sizer_main.AddGrowableCol( 0 )
        sizer_main.AddGrowableRow( 1 )

        self.SetSizer( sizer_main )
        self.Layout()
        sizer_main.Fit( self )
        self.sizer_main = sizer_main

        self.Centre( wx.BOTH )

        # Connect Events
        self.sizer_btnsNo.Bind( wx.EVT_BUTTON, self.on_clear_selected )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def on_clear_selected( self, event ):
        event.Skip()


