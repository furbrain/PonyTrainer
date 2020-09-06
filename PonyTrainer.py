#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import platform
import subprocess
import time
from inspect import cleandoc

import wx
import wx.stc
import os
import sys
import datetime
import webbrowser
import json
from functools import partial

from src import gui
from src import importer
from src import svxtextctrl
from src import bootloader
from src import hexfile
from src import config
from src import calibration
from src import struct_parser
from src import version
from src import client_config
from pyupdater import client

from src.version import Version


class ActualMainFrame(gui.PonyFrame):
    def __init__(self, asset_folder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asset_folder = asset_folder
        try:
            self.hexfile = hexfile.HexFile(os.path.join(self.asset_folder, "firmware.hex"))
        except (IOError, hexfile.HexFileError):
            self.hexfile = None
            self.frame_statusbar.SetStatusText("No firmware available",2)
        else:
            v = version.Version.from_data_source(self.hexfile)
            self.frame_statusbar.SetStatusText(f"Available Firmware: {v.as_semantic()}",2)
        self.notebook.DeleteAllPages()
        self.bootloader = None
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.check_bootloader, self.timer)
        self.timer.Start(1000)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        
    def create_pane(self, pane=None, ctrl = None, focus=True):
        if pane is None:
            new_page = True
            pane = wx.Panel(self.notebook, wx.ID_ANY)
        else:
            new_page = False
        if ctrl is None:
            ctrl = svxtextctrl.SVXTextCtrl(pane)
        else:
            ctrl.Reparent(pane)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(ctrl, 1, wx.EXPAND, 0)
        pane.SetSizer(sizer)
        pane.ctrl = ctrl
        ctrl.Bind(wx.stc.EVT_STC_SAVEPOINTREACHED, lambda x: self.set_pane_title(pane, ctrl))
        ctrl.Bind(wx.stc.EVT_STC_SAVEPOINTLEFT, lambda x: self.set_pane_title(pane, ctrl))
        if new_page:
            self.notebook.AddPage(pane, ctrl.GetTitle())
        if focus:
            index = self.notebook.FindPage(pane)
            self.notebook.SetSelection(index)
        return pane
        
    def get_active_ctrl(self):
        index = self.notebook.GetSelection()
        pane = self.notebook.GetPage(index)
        return pane.ctrl
        
    def set_pane_title(self, pane, ctrl):
        index = self.notebook.FindPage(pane)
        self.notebook.SetPageText(index, ctrl.GetTitle())
        
    def check_bootloader(self, event):
        if self.bootloader is None:
            try:
                self.bootloader = bootloader.Programmer()
            except bootloader.ProgrammerError:
                pass
            else:
                self.frame_statusbar.SetStatusText("Connected to " + self.bootloader.get_name(), 0)
                v = version.Version.from_data_source(self.bootloader)
                self.frame_statusbar.SetStatusText(f"Device Firmware: {v.as_semantic()}", 1)
        else:
            try:
                self.bootloader.read_program(0x9d000000,1)
            except IOError:
                self.bootloader = None
                self.frame_statusbar.SetStatusText("Disconnected", 0)
                self.frame_statusbar.SetStatusText("Device Firmware: ---", 1)

    def no_pony_error(self):
        msg = wx.MessageDialog(self, "No Pony attached").ShowModal()
                
    def Import(self, event):
        if self.bootloader is None:
            self.no_pony_error()
            return
        dlg = importer.ActualImportDialog(self, self.bootloader)
        if dlg.ShowModal()==wx.ID_OK:
            texts = dlg.get_texts(None)
            for title, text in texts:
                ctrl = svxtextctrl.SVXTextCtrl(self, text = text, filename = title)
                self.create_pane(ctrl=ctrl)
                ctrl.named = False
        
    def OnClose(self, event):
        if event.CanVeto():
            for i in range(self.notebook.GetPageCount()):
                pane = self.notebook.GetPage(i)
                if not pane.ctrl.CanClose():
                    event.Veto()
                    return
        self.Destroy()
        
    def OnQuit(self, event):
        self.Close()
    
    def DeviceSettings(self, event):
        dlg = gui.DeviceSettingsDialog(self)
        dlg.ShowModal()
        
    def DeviceGetCalibration(self, event):
        if self.bootloader is None:
            self.no_pony_error()
            return
        data = {'name': self.bootloader.get_name(),
                'shots': calibration.read_cal(self.bootloader),
                'conf': config.get_config(self.bootloader)}
        with wx.FileDialog(self, "Save Calibration", wildcard="Calibration file (*.cal)|*.cal",
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            try:
                with open(fileDialog.GetPath(),"w") as f:
                     json.dump(data,f,cls=struct_parser.StructEncoder)
            except IOError as e:
                wx.MessageDialog(self, "Failed to save file:\n%s" % e).ShowModal()
                
    def About(self, event):
        gui.AboutDialog(self).ShowModal()

    def OnNew(self, event):  # wxGlade: PonyFrame.<event_handler>
        self.create_pane()

    def OnOpen(self, event):  # wxGlade: PonyFrame.<event_handler>
        with wx.FileDialog(self, "Open SVX file", wildcard="Survex files (*.svx)|*.svx",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return     # the user changed their mind

                # Proceed loading the file chosen by the user
                pathname = fileDialog.GetPath()
                ctrl = svxtextctrl.SVXTextCtrl(self, filename=pathname)
                try:
                    ctrl.LoadFile(pathname)
                except IOError as e:
                    wx.MessageDialog(self, "Failed to load file:\n%s" % e).ShowModal()
                else:
                    self.create_pane(ctrl=ctrl)

    def OnRevert(self, event):  # wxGlade: PonyFrame.<event_handler>
        ctrl = self.get_active_ctrl()
        if not ctrl.named: return
        if ctrl.IsModified():
            message = "Revert changes to %s" % os.path.basename(ctrl.filename)
            if wx.MessageBox(message, "Revert File", wx.YES_NO) == wx.YES:
                try:
                    ctrl.LoadFile(ctrl.filename)
                except IOError as e:
                    wx.MessageDialog(self, "Failed to load file:\n%s" % e).ShowModal()

    def OnSave(self, event):  # wxGlade: PonyFrame.<event_handler>
        ctrl = self.get_active_ctrl()
        ctrl.OnSave()
                    
    def OnSaveAs(self, event):  # wxGlade: PonyFrame.<event_handler>
        ctrl = self.get_active_ctrl()
        ctrl.OnSaveAs()

    def OnClosePane(self, event):  # wxGlade: PonyFrame.<event_handler>
        ctrl = self.get_active_ctrl()
        if ctrl.CanClose():
            self.notebook.DeletePage(self.notebook.GetSelection())

    def OnCut(self, event):  # wxGlade: PonyFrame.<event_handler>
        ctrl = self.get_active_ctrl()
        ctrl.Cut()

    def OnCopy(self, event):  # wxGlade: PonyFrame.<event_handler>
        ctrl = self.get_active_ctrl()
        ctrl.Copy()

    def OnPaste(self, event):  # wxGlade: PonyFrame.<event_handler>
        ctrl = self.get_active_ctrl()
        ctrl.Paste()

    def DeviceUploadFirmware(self, event):  # wxGlade: PonyFrame.<event_handler>
        if self.bootloader is None:
            self.no_pony_error()
            return
        if self.hexfile is None:
            wx.MessageBox("Firmware not found")
            return

        # check versions
        current_ver = Version.from_data_source(self.bootloader)
        next_ver = Version.from_data_source(self.hexfile)
        if current_ver >= next_ver:
            if wx.MessageBox(cleandoc(f"""
                                Your current version is {current_ver.as_semantic()},
                                but you are trying to install {next_ver.as_semantic()}.
                                Are you sure you want to proceed?"""),
                             caption="Firmware version conflict",
                             style=wx.YES_NO | wx.CENTER | wx.NO_DEFAULT) == wx.NO:
                return
        if wx.MessageBox("Are you sure you want to upgrade your firmware?\n"
                         "You may lose any data and will need to re-calibrate",
                         caption="Upgrade Firmware",
                         style=wx.OK | wx.CANCEL) == wx.CANCEL:
            return
        offset = self.bootloader.user_range[0]
        maximum = self.bootloader.user_range[1]-offset
        try:
            with wx.ProgressDialog("Updating Firmware", "Writing...", maximum) as dlg:
                self.bootloader.write_program(self.hexfile, set_progress=lambda x: dlg.Update(x-offset))
                dlg.Update(0,"Verifying...")
                self.bootloader.verify_program(self.hexfile,set_progress=lambda x: dlg.Update(x-offset))
                self.bootloader.write_datetime(datetime.datetime.now())
            wx.MessageBox("Programming complete")
        except bootloader.ProgrammerError as e:
            wx.MessageBox("Firmware update failed\n%s" % e, "Error")
                
    def DeviceSetClock(self, event):
        if self.bootloader is None:
            self.no_pony_error()
            return
        dt = datetime.datetime.now()
        self.bootloader.write_datetime(dt)
        wx.MessageBox("%s Clock set to %s" % (self.bootloader.get_name(),dt.strftime("%Y-%m-%d %H:%M")))

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)


    def fix_env(self):
        lib_key = "LD_LIBRARY_PATH"
        self.env_backup = os.environ.get(lib_key)
        orig = os.environ.get(lib_key + "_ORIG")
        if orig is None:
            os.environ.pop(lib_key)
        else:
            os.environ[lib_key] = orig

    def restore_env(self):
        os.environ["LD_LIBRARY_PATH"] = self.env_backup

    def ShowManual(self, event):  # wxGlade: PonyFrame.<event_handler>
        manual = os.path.join(self.asset_folder, "manual.pdf")
        self.fix_env()
        webbrowser.open(manual)
        self.restore_env()


class ProgressMonitor:
    def __init__(self):
        self.dlg = None
        self.title = "Downloading"
        self.asset = "PonyTrainer"

    def update(self, data):
        if self.dlg is None:
            self.dlg = wx.ProgressDialog(self.title,"Starting download", maximum=data["total"], style=wx.PD_APP_MODAL)
            self.dlg.Show()
        elif data["status"]=="finished":
            self.dlg.Close()
            self.dlg = None
            return
        elif data["downloaded"] == data["total"]:
            status = f"{self.asset.capitalize()} download complete"
        else:
            status = f"Downloading {self.asset}"
        self.dlg.Update(data["downloaded"],newmsg=status)

PonyTrainer = wx.App(False)
monitor = ProgressMonitor()
update_config = client_config.ClientConfig()
update_client = client.Client(client_config.ClientConfig(), refresh=True, progress_hooks=[monitor.update])
app_update = update_client.update_check(update_config.APP_NAME, version.SOFTWARE_VERSION)
asset_folder = update_client.update_folder
if client.FROZEN and app_update:
    if wx.MessageBox("There is a new version available, update?", "New version", wx.YES_NO)==wx.YES:
        monitor.title = "Updating PonyTrainer"
        monitor.asset = "PonyTrainer"
        app_update.download()
        if app_update.is_downloaded():
            app_update.extract_restart()
        else:
            wx.MessageBox("Could not download, starting as normal")

for asset in ("manual", "firmware"):
    monitor.title = "Getting latest " + asset
    monitor.asset = asset
    asset_update = update_client.update_check(asset, "0.0.0")
    if asset_update is not None:
        if not asset_update.is_downloaded():
            asset_update.download()
            if asset_update.is_downloaded():
                asset_update.extract()

frame = ActualMainFrame(asset_folder, None, wx.ID_ANY, "PonyTrainer")
PonyTrainer.SetTopWindow(frame)
frame.Show()
PonyTrainer.MainLoop()        
