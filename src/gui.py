#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.4 on Fri Sep  4 11:40:49 2020
#

import wx
import wx.adv

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
from .svxtextctrl import SVXTextCtrl
import wx.lib.docview
from . import version
# end wxGlade


class PonyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: PonyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((800, 600))
        
        # Menu Bar
        self.frame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.ID_NEW, "&New", "")
        self.Bind(wx.EVT_MENU, self.OnNew, id=wx.ID_NEW)
        wxglade_tmp_menu.Append(wx.ID_OPEN, "&Open", "")
        self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "&Import\tCtrl-I", "")
        self.Bind(wx.EVT_MENU, self.Import, id=item.GetId())
        wxglade_tmp_menu.Append(wx.ID_REVERT, "&Revert", "")
        self.Bind(wx.EVT_MENU, self.OnRevert, id=wx.ID_REVERT)
        wxglade_tmp_menu.Append(wx.ID_SAVE, "&Save", "")
        self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)
        wxglade_tmp_menu.Append(wx.ID_SAVEAS, "Save &as", "")
        self.Bind(wx.EVT_MENU, self.OnSaveAs, id=wx.ID_SAVEAS)
        wxglade_tmp_menu.Append(wx.ID_CLOSE, "&Close", "")
        self.Bind(wx.EVT_MENU, self.OnClosePane, id=wx.ID_CLOSE)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(wx.ID_EXIT, "&Quit", "")
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)
        self.frame_menubar.Append(wxglade_tmp_menu, "&File")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.ID_CUT, "Cu&t\tCtrl-X", "")
        self.Bind(wx.EVT_MENU, self.OnCut, id=wx.ID_CUT)
        wxglade_tmp_menu.Append(wx.ID_COPY, "&Copy", "")
        self.Bind(wx.EVT_MENU, self.OnCopy, id=wx.ID_COPY)
        wxglade_tmp_menu.Append(wx.ID_PASTE, "&Paste", "")
        self.Bind(wx.EVT_MENU, self.OnPaste, id=wx.ID_PASTE)
        self.frame_menubar.Append(wxglade_tmp_menu, "&Edit")
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "&Upload Firmware", "")
        self.Bind(wx.EVT_MENU, self.DeviceUploadFirmware, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "&Get Calibration", "")
        self.Bind(wx.EVT_MENU, self.DeviceGetCalibration, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Set &Clock", "")
        self.Bind(wx.EVT_MENU, self.DeviceSetClock, id=item.GetId())
        self.frame_menubar.Append(wxglade_tmp_menu, "&Device")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.ID_HELP, "&Manual", "")
        self.Bind(wx.EVT_MENU, self.ShowManual, id=wx.ID_HELP)
        wxglade_tmp_menu.Append(wx.ID_ABOUT, "&About", "")
        self.Bind(wx.EVT_MENU, self.About, id=wx.ID_ABOUT)
        self.frame_menubar.Append(wxglade_tmp_menu, "&Help")
        self.SetMenuBar(self.frame_menubar)
        # Menu Bar end
        self.frame_statusbar = self.CreateStatusBar(3)
        
        # Tool Bar
        self.frame_toolbar = wx.ToolBar(self, -1)
        self.SetToolBar(self.frame_toolbar)
        self.frame_toolbar.AddTool(wx.ID_SAVE, "Save", wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, wx.DefaultSize), wx.NullBitmap, wx.ITEM_NORMAL, "Save", "")
        self.frame_toolbar.AddTool(wx.ID_BOTTOM, "Import", wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, wx.DefaultSize), wx.NullBitmap, wx.ITEM_NORMAL, "Import from Pony", "")
        self.frame_toolbar.AddTool(wx.ID_EXIT, "Quit", wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR, wx.DefaultSize), wx.NullBitmap, wx.ITEM_NORMAL, "OnQuit", "")
        self.frame_toolbar.AddSeparator()
        self.frame_toolbar.AddTool(wx.ID_CUT, "Cut", wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_TOOLBAR, wx.DefaultSize), wx.NullBitmap, wx.ITEM_NORMAL, "Cut", "")
        self.frame_toolbar.AddTool(wx.ID_COPY, "Copy", wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, wx.DefaultSize), wx.NullBitmap, wx.ITEM_NORMAL, "Copy", "")
        self.frame_toolbar.AddTool(wx.ID_PASTE, "Paste", wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, wx.DefaultSize), wx.NullBitmap, wx.ITEM_NORMAL, "Paste", "")
        # Tool Bar end
        self.notebook = wx.Notebook(self, wx.ID_ANY)
        self.notebook_first_pane = wx.Panel(self.notebook, wx.ID_ANY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TOOL, self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_TOOL, self.Import, id=wx.ID_BOTTOM)
        self.Bind(wx.EVT_TOOL, self.OnCut, id=wx.ID_CUT)
        self.Bind(wx.EVT_TOOL, self.OnCopy, id=wx.ID_COPY)
        self.Bind(wx.EVT_TOOL, self.OnPaste, id=wx.ID_PASTE)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: PonyFrame.__set_properties
        self.SetTitle("PonyTrainer")
        self.frame_statusbar.SetStatusWidths([-2, -1, -1])

        # statusbar fields
        frame_statusbar_fields = ["Disconnected", "Device firmware: ---", "Available firmware: ---"]
        for i in range(len(frame_statusbar_fields)):
            self.frame_statusbar.SetStatusText(frame_statusbar_fields[i], i)
        self.frame_toolbar.Realize()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: PonyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.notebook.AddPage(self.notebook_first_pane, "Untitled")
        sizer_1.Add(self.notebook, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def OnNew(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'OnNew' not implemented!")
        event.Skip()

    def OnOpen(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'OnOpen' not implemented!")
        event.Skip()

    def Import(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'Import' not implemented!")
        event.Skip()

    def OnRevert(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'OnRevert' not implemented!")
        event.Skip()

    def OnSave(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'OnSave' not implemented!")
        event.Skip()

    def OnSaveAs(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'OnSaveAs' not implemented!")
        event.Skip()

    def OnClosePane(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'OnClosePane' not implemented!")
        event.Skip()

    def OnQuit(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'OnQuit' not implemented!")
        event.Skip()

    def OnCut(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'OnCut' not implemented!")
        event.Skip()

    def OnCopy(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'OnCopy' not implemented!")
        event.Skip()

    def OnPaste(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'OnPaste' not implemented!")
        event.Skip()

    def DeviceUploadFirmware(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'DeviceUploadFirmware' not implemented!")
        event.Skip()

    def DeviceGetCalibration(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'DeviceGetCalibration' not implemented!")
        event.Skip()

    def DeviceSetClock(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'DeviceSetClock' not implemented!")
        event.Skip()

    def ShowManual(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'ShowManual' not implemented!")
        event.Skip()

    def About(self, event):  # wxGlade: PonyFrame.<event_handler>
        print("Event handler 'About' not implemented!")
        event.Skip()

# end of class PonyFrame

class AboutDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: AboutDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((412, 147))
        self.label_1 = wx.StaticText(self, wx.ID_ANY, "PonyTrainer version not set", style=wx.ALIGN_CENTER)
        self.label_1.SetLabel("PonyTrainer " + version.SOFTWARE_VERSION)
        self.hyperlink_1 = wx.adv.HyperlinkCtrl(self, wx.ID_ANY, "http://www.shetlandattackpony.co.uk/", "", style=wx.adv.HL_ALIGN_CENTRE)
        self.button_1 = wx.Button(self, wx.ID_OK, "")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: AboutDialog.__set_properties
        self.SetTitle("About")
        self.SetSize((412, 147))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: AboutDialog.__do_layout
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.label_1, 1, wx.EXPAND, 0)
        sizer_2.Add(self.hyperlink_1, 1, wx.ALIGN_CENTER, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, u"© 2019 Phil Underwood", style=wx.ALIGN_CENTER)
        sizer_2.Add(label_2, 1, wx.EXPAND, 0)
        sizer_2.Add(self.button_1, 0, wx.ALIGN_CENTER | wx.ALL, 1)
        self.SetSizer(sizer_2)
        self.Layout()
        self.Centre()
        # end wxGlade

# end of class AboutDialog

class ImportDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ImportDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((545, 427))
        self.survey_list = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_SORT_DESCENDING | wx.LC_VRULES)
        self.advanced = wx.CheckBox(self, wx.ID_ANY, "Advanced")
        self.advanced_controls = wx.Panel(self, wx.ID_ANY)
        self.angles = wx.RadioBox(self.advanced_controls, wx.ID_ANY, "Angles", choices=["From Pony", "Polar", "Grad", "Cartesian"], majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.units = wx.RadioBox(self.advanced_controls, wx.ID_ANY, "Length Units", choices=["From Pony", "Metric", "Imperial"], majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.button_2 = wx.Button(self, wx.ID_OK, "")
        self.button_3 = wx.Button(self, wx.ID_CANCEL, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHECKBOX, lambda x: (self.advanced_controls.Show(x.IsChecked()), self.__do_layout()), self.advanced)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ImportDialog.__set_properties
        self.SetTitle("Import Surveys")
        self.SetSize((545, 427))
        self.survey_list.AppendColumn("Date", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.survey_list.AppendColumn("Stations", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.survey_list.AppendColumn("Legs", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.angles.SetSelection(0)
        self.units.SetSelection(0)
        self.advanced_controls.Hide()
        self.button_2.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ImportDialog.__do_layout
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Surveys"), wx.HORIZONTAL)
        sizer_6.Add(self.survey_list, 1, wx.EXPAND, 0)
        sizer_3.Add(sizer_6, 1, wx.ALL | wx.EXPAND, 3)
        sizer_3.Add(self.advanced, 0, wx.ALL, 3)
        sizer6.Add(self.angles, 1, wx.ALL | wx.EXPAND, 3)
        sizer6.Add(self.units, 1, wx.ALL | wx.EXPAND, 3)
        self.advanced_controls.SetSizer(sizer6)
        sizer_3.Add(self.advanced_controls, 1, wx.ALL | wx.EXPAND, 3)
        sizer_4.Add(self.button_2, 0, 0, 0)
        sizer_4.Add(self.button_3, 0, 0, 0)
        sizer_3.Add(sizer_4, 0, wx.ALIGN_RIGHT | wx.ALL, 3)
        self.SetSizer(sizer_3)
        self.Layout()
        # end wxGlade

# end of class ImportDialog

if __name__ == "__main__":
    PonyTrainer = wx.PySimpleApp()
    frame = PonyFrame(None, wx.ID_ANY, "")
    PonyTrainer.SetTopWindow(frame)
    frame.Show()
    PonyTrainer.MainLoop()
