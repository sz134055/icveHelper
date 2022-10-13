# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class main
###########################################################################

class main ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"登录至ICVE", pos = wx.DefaultPosition, size = wx.Size( 776,535 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        main_layout = wx.BoxSizer( wx.VERTICAL )

        account_layout = wx.BoxSizer( wx.HORIZONTAL )

        account_input_panel = wx.BoxSizer( wx.HORIZONTAL )

        self.a_input_label = wx.StaticText( self, wx.ID_ANY, u"账号", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.a_input_label.Wrap( -1 )

        self.a_input_label.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )

        account_input_panel.Add( self.a_input_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.account_input = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER )
        account_input_panel.Add( self.account_input, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        account_layout.Add( account_input_panel, 1, wx.EXPAND, 5 )

        pswd_input_panel = wx.BoxSizer( wx.HORIZONTAL )

        self.p_input_label = wx.StaticText( self, wx.ID_ANY, u"密码", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.p_input_label.Wrap( -1 )

        self.p_input_label.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )

        pswd_input_panel.Add( self.p_input_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.pswd_input = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER|wx.TE_PASSWORD )
        pswd_input_panel.Add( self.pswd_input, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        account_layout.Add( pswd_input_panel, 1, wx.EXPAND, 5 )

        login_btn_panel = wx.BoxSizer( wx.HORIZONTAL )

        self.login_btn = wx.Button( self, wx.ID_ANY, u"登录", wx.DefaultPosition, wx.DefaultSize, 0 )
        login_btn_panel.Add( self.login_btn, 0, wx.ALL, 5 )

        self.login_params_btn = wx.Button( self, wx.ID_ANY, u"登录参数配置", wx.DefaultPosition, wx.DefaultSize, 0 )
        login_btn_panel.Add( self.login_params_btn, 0, wx.ALL, 5 )

        self.help_btn = wx.Button( self, wx.ID_ANY, u"说明", wx.DefaultPosition, wx.DefaultSize, 0 )
        login_btn_panel.Add( self.help_btn, 0, wx.ALL, 5 )


        account_layout.Add( login_btn_panel, 1, wx.EXPAND, 5 )


        main_layout.Add( account_layout, 0, 0, 5 )

        account_Info = wx.BoxSizer( wx.HORIZONTAL )

        info_panel_left = wx.BoxSizer( wx.HORIZONTAL )

        self.info_user_label = wx.StaticText( self, wx.ID_ANY, u"登录为：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.info_user_label.Wrap( -1 )

        self.info_user_label.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )

        info_panel_left.Add( self.info_user_label, 0, wx.ALL, 5 )

        self.info_user = wx.StaticText( self, wx.ID_ANY, u"等待登录", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.info_user.Wrap( -1 )

        self.info_user.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )

        info_panel_left.Add( self.info_user, 0, wx.ALL, 5 )


        account_Info.Add( info_panel_left, 1, 0, 5 )

        info_panel_center = wx.BoxSizer( wx.HORIZONTAL )

        self.info_id_panel = wx.StaticText( self, wx.ID_ANY, u"ID：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.info_id_panel.Wrap( -1 )

        self.info_id_panel.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )

        info_panel_center.Add( self.info_id_panel, 0, wx.ALL, 5 )

        self.info_id = wx.StaticText( self, wx.ID_ANY, u"等待登录", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.info_id.Wrap( -1 )

        self.info_id.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )

        info_panel_center.Add( self.info_id, 0, wx.ALL, 5 )


        account_Info.Add( info_panel_center, 1, 0, 5 )


        main_layout.Add( account_Info, 0, wx.EXPAND, 5 )

        list_layout = wx.BoxSizer( wx.VERTICAL )

        list_layout.SetMinSize( wx.Size( -1,350 ) )
        list_sub_layout = wx.BoxSizer( wx.HORIZONTAL )

        list_sub_layout.SetMinSize( wx.Size( -1,350 ) )
        course_list_layout = wx.BoxSizer( wx.VERTICAL )

        course_list_layout.SetMinSize( wx.Size( 300,-1 ) )
        course_listChoices = []
        self.course_list = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, course_listChoices, 0 )
        course_list_layout.Add( self.course_list, 1, wx.ALL|wx.EXPAND, 5 )


        list_sub_layout.Add( course_list_layout, 1, wx.EXPAND, 5 )

        func_layout = wx.BoxSizer( wx.VERTICAL )

        self.func_tips_1 = wx.StaticText( self, wx.ID_ANY, u"等待登录", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.func_tips_1.Wrap( -1 )

        self.func_tips_1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )

        func_layout.Add( self.func_tips_1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.func_tips_2 = wx.StaticText( self, wx.ID_ANY, u">>>", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        self.func_tips_2.Wrap( -1 )

        self.func_tips_2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )

        func_layout.Add( self.func_tips_2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.flash_course_btn = wx.Button( self, wx.ID_ANY, u"刷新课程列表", wx.DefaultPosition, wx.DefaultSize, 0 )
        func_layout.Add( self.flash_course_btn, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.func_start_btn = wx.Button( self, wx.ID_ANY, u"开始完成课件", wx.DefaultPosition, wx.DefaultSize, 0 )
        func_layout.Add( self.func_start_btn, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        list_sub_layout.Add( func_layout, 1, 0, 5 )

        cell_layout = wx.BoxSizer( wx.VERTICAL )

        cell_layout.SetMinSize( wx.Size( 300,-1 ) )
        cell_listChoices = []
        self.cell_list = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cell_listChoices, 0 )
        cell_layout.Add( self.cell_list, 1, wx.ALL|wx.EXPAND, 5 )


        list_sub_layout.Add( cell_layout, 1, wx.EXPAND, 5 )


        list_layout.Add( list_sub_layout, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        main_layout.Add( list_layout, 1, wx.EXPAND, 5 )

        running_tips_layout = wx.BoxSizer( wx.VERTICAL )

        self.running_tips = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.running_tips.Wrap( -1 )

        self.running_tips.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )

        running_tips_layout.Add( self.running_tips, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        main_layout.Add( running_tips_layout, 1, wx.EXPAND, 5 )

        gauge_layout = wx.BoxSizer( wx.VERTICAL )

        total_gauge_layout = wx.BoxSizer( wx.HORIZONTAL )

        self.total_gauge_label = wx.StaticText( self, wx.ID_ANY, u"总进度   ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.total_gauge_label.Wrap( -1 )

        self.total_gauge_label.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )

        total_gauge_layout.Add( self.total_gauge_label, 0, wx.ALL, 5 )

        self.total_gauge = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 500,-1 ), wx.GA_HORIZONTAL )
        self.total_gauge.SetValue( 0 )
        total_gauge_layout.Add( self.total_gauge, 0, wx.ALL, 5 )

        self.total_gague_persentage = wx.StaticText( self, wx.ID_ANY, u"0%", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.total_gague_persentage.Wrap( -1 )

        self.total_gague_persentage.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
        self.total_gague_persentage.SetMinSize( wx.Size( 40,-1 ) )

        total_gauge_layout.Add( self.total_gague_persentage, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        gauge_layout.Add( total_gauge_layout, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

        cell_gauge_layout = wx.BoxSizer( wx.HORIZONTAL )

        self.cell_gauge_label = wx.StaticText( self, wx.ID_ANY, u"课件进度", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cell_gauge_label.Wrap( -1 )

        self.cell_gauge_label.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )

        cell_gauge_layout.Add( self.cell_gauge_label, 0, wx.ALL, 5 )

        self.cell_gauge = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 500,-1 ), wx.GA_HORIZONTAL )
        self.cell_gauge.SetValue( 0 )
        cell_gauge_layout.Add( self.cell_gauge, 1, wx.ALL, 5 )

        self.cell_gauge_persentage = wx.StaticText( self, wx.ID_ANY, u"0%", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cell_gauge_persentage.Wrap( -1 )

        self.cell_gauge_persentage.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
        self.cell_gauge_persentage.SetMinSize( wx.Size( 40,-1 ) )

        cell_gauge_layout.Add( self.cell_gauge_persentage, 0, wx.ALL, 5 )


        gauge_layout.Add( cell_gauge_layout, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        main_layout.Add( gauge_layout, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( main_layout )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.login_btn.Bind( wx.EVT_BUTTON, self.login )
        self.login_params_btn.Bind( wx.EVT_BUTTON, self.login_params )
        self.help_btn.Bind( wx.EVT_BUTTON, self.help )
        self.course_list.Bind( wx.EVT_LISTBOX, self.get_cell_list )
        self.flash_course_btn.Bind( wx.EVT_BUTTON, self.flash_course_list )
        self.func_start_btn.Bind( wx.EVT_BUTTON, self.finish_course )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def login( self, event ):
        event.Skip()

    def login_params( self, event ):
        event.Skip()

    def help( self, event ):
        event.Skip()

    def get_cell_list( self, event ):
        event.Skip()

    def flash_course_list( self, event ):
        event.Skip()

    def finish_course( self, event ):
        event.Skip()


