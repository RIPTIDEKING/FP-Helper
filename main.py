
import numpy as np
import pyautogui as SS
import time
import cv2

from Snip import SnipFrame
from EditImage import EditImageFrame

from PIL import Image as Pimage


import wx
from wx.core import STAY_ON_TOP

import time

class DashboardFrame(wx.Frame):

    def __init__(self,parent,title = '',size = (600,400)):
        super().__init__(None,title = title,size = size)

        self.parent = parent
        self.Bind(wx.EVT_CLOSE,self.parent.onClose)

        self.panel = wx.Panel(self)
        self.uploadBtn = wx.Button(self.panel,label = 'Upload')
        self.uploadBtn.Bind(wx.EVT_BUTTON,self.onClickedUpload)
        
        self.snipBtn = wx.Button(self.panel,label = 'Snip')
        self.snipBtn.Bind(wx.EVT_BUTTON,self.onClickedSnip)

        hbox = wx.BoxSizer()
        hbox.AddStretchSpacer()
        hbox.Add(self.uploadBtn,0,wx.ALIGN_CENTER)
        hbox.AddStretchSpacer()
        hbox.Add(self.snipBtn,0,wx.ALIGN_CENTER)
        hbox.AddStretchSpacer()
        self.panel.SetSizer(hbox)
    
    def onInit(self):
        self.parent.image_frame = EditImageFrame(self.parent,title='FP-Helper')

    def onClickedUpload(self,event):
        fileDialog = wx.FileDialog(self, "Open PNG file", wildcard="PNG files (*.png)|*.png",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return     

        
        pathname = fileDialog.GetPath()

        try:
            ssImage = wx.Bitmap(pathname, wx.BITMAP_TYPE_ANY)
            self.parent.image_frame.showImage(ssImage)
        except IOError:
            wx.LogError("Cannot open file '%s'." % pathname)

    def onClickedSnip(self,event):
        self.Hide()
        print(self.parent.ss_frame.IsFullScreen())

        if not self.parent.ss_frame.IsFullScreen():
            self.parent.ss_frame.ShowFullScreen(not self.parent.ss_frame.IsFullScreen())        
            self.parent.ss_frame.SetTransparent(50)
            self.parent.SetTopWindow(self.parent.ss_frame)
        else:
            self.parent.ss_frame.Show()
            self.parent.ss_frame.SetTransparent(50)
            self.parent.SetTopWindow(self.parent.ss_frame)
            self.parent.ss_frame.onInit()
        



class MyApp(wx.App):

    def OnInit(self):
        self.dashboard_frame = DashboardFrame(self,title='FP-Helper')
        self.ss_frame = SnipFrame(self,title='FP-Helper')
        self.image_frame = EditImageFrame(self,title='FP-Helper')

        # self.dashboard_frame.ss_frame = self.ss_frame
        # self.ss_frame.image_frame = self.image_frame
        # self.image_frame.dashboard_frame = self.dashboard_frame
        
        self.dashboard_frame.Show()
        # self.dashboard_frame.ShowFullScreen(True)
        return True

    def onClose(self,event):
        wx.Exit()

app = MyApp(0)
app.MainLoop()