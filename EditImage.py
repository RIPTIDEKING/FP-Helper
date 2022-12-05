import wx
import time

class EditImageFrame(wx.Frame):

    def __init__(self, parent = None, title= ""):
        super().__init__(None,size= wx.DisplaySize(),title = title)

        self.parent = parent
        self.Bind(wx.EVT_CLOSE,self.parent.onClose)
        self.toggleStamp = False
        

    def showImage(self,img):
        self.bgpanel = wx.Panel(self,size = self.GetSize())
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        imgPanel = self.imgPanelCreate(img)
        optionsPanel = self.optionsPanelCreate()
        # imgPanel.SetBackgroundColour(wx.Colour(0,100,0))

        vbox.Add(imgPanel,19,wx.EXPAND)
        vbox.Add(optionsPanel,1,wx.EXPAND)
        self.bgpanel.SetSizer(vbox)

        self.Show()


    def imgPanelCreate(self,img):
        imgPanel = wx.Panel(self.bgpanel)

        editableImagePanel = wx.Panel(imgPanel,size = img.GetSize())
        editableImagePanel.Bind(wx.EVT_LEFT_DOWN,self.onStamping)
        self.stamping = Stamping(editableImagePanel,img)

        ver_box = wx.BoxSizer(wx.VERTICAL)
        ver_box.AddStretchSpacer(prop=1)
        ver_box.Add(editableImagePanel,flag = wx.ALIGN_CENTER)
        ver_box.AddStretchSpacer(prop=1)
        imgPanel.SetSizer(ver_box)

        return imgPanel

    def optionsPanelCreate(self):
        optionsPanel = wx.Panel(self.bgpanel)
        
        stampBtn = wx.ToggleButton(optionsPanel,label = 'Stamp')
        stampBtn.Bind(wx.EVT_TOGGLEBUTTON, self.onStampToggle)

        stampSize = wx.SpinCtrl(optionsPanel,value = str(self.stamping.radius))
        stampSize.Bind(wx.EVT_SPINCTRL,self.onSizeChanged)

        stampColor = wx.ComboBox(optionsPanel,value = 'Green',choices = self.stamping.colors)
        stampColor.Bind(wx.EVT_COMBOBOX,self.onColorSelect)

        newBtn = wx.Button(optionsPanel,label = 'New Image')
        newBtn.Bind(wx.EVT_BUTTON,self.onNewBtn)

        saveBtn = wx.Button(optionsPanel,label = 'Save')
        saveBtn.Bind(wx.EVT_BUTTON,self.stamping.OnSave)

        hor_box = wx.BoxSizer()
        hor_box.AddStretchSpacer()
        hor_box.Add(stampBtn,0,wx.ALIGN_CENTER)
        hor_box.AddSpacer(20)
        hor_box.Add(stampSize,0,wx.ALIGN_CENTER)
        hor_box.AddSpacer(20)
        hor_box.Add(stampColor,0,wx.ALIGN_CENTER)
        hor_box.AddSpacer(20)
        hor_box.Add(saveBtn,0,wx.ALIGN_CENTER)
        hor_box.AddSpacer(20)
        hor_box.Add(newBtn,0,wx.ALIGN_CENTER)
        hor_box.AddStretchSpacer()
        optionsPanel.SetSizer(hor_box)

        return optionsPanel

    def onStampToggle(self,event):
        self.toggleStamp = not self.toggleStamp

    def onStamping(self,event):
        if not self.toggleStamp: return
        self.stamping.addStamp(event.GetPosition())

    def onSizeChanged(self,event):
        size = event.GetPosition()
        if size < 5:
            size = 5
        self.stamping.radius = size
        self.stamping.parent.Refresh()
    
    def onColorSelect(self,event):
        print(event.GetInt())
        self.stamping.selected = event.GetInt()
    
    def onNewBtn(self,event):
        self.Hide()
        self.Destroy()
        self.parent.dashboard_frame.Show()
        # self.dashboard_frame.ShowFullScreen(True)
        # self.parent.SetTopWindow(self.dashboard_frame)

class Stamping:


    def __init__(self,parent,image):
        
        self.cords = []
        self.parent = parent
        self.image = image
        self.parent.Bind(wx.EVT_PAINT,self.OnPaint)
        self.radius = 15

        self.initColors()
        counts = len(self.stampColors)

        for i in range(counts):
            temp = []
            self.cords.append(temp)

        self.selected = 0
    

    def addStamp(self,cord):
        self.cords[self.selected].append(cord)
        self.parent.Refresh()

    def OnPaint(self, event):

        dc = wx.PaintDC(self.parent)
        

        font = wx.Font(self.radius,wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        dc.SetTextForeground(wx.WHITE)
        
        dc.DrawBitmap(self.image,0,0)
        for ind,cords in enumerate(self.cords):
            dc.SetPen(wx.Pen(self.stampColors[ind][0], 2))
            dc.SetBrush(wx.Brush(self.stampColors[ind][1]))
            for index,pnt in enumerate(cords):
                dc.DrawCircle(pnt,self.radius)
                offset = dc.GetTextExtent(str(index+1))
                dc.DrawText(str(index+1),pnt.x-offset.x/2,pnt.y-offset.y/2)

    def OnSave(self, event):

        saveimg = wx.Bitmap(self.parent.GetSize())
        dc = wx.MemoryDC(saveimg)
        

        font = wx.Font(self.radius,wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        dc.SetTextForeground(wx.WHITE)
        
        dc.DrawBitmap(self.image,0,0)
        for ind,cords in enumerate(self.cords):
            dc.SetPen(wx.Pen(self.stampColors[ind][0], 2))
            dc.SetBrush(wx.Brush(self.stampColors[ind][1]))
            for index,pnt in enumerate(cords):
                dc.DrawCircle(pnt,self.radius)
                offset = dc.GetTextExtent(str(index+1))
                dc.DrawText(str(index+1),pnt.x-offset.x/2,pnt.y-offset.y/2)
        fname = "Edited_SS{}.png".format(int(round(time.time()*1000)))
        saveimg.SaveFile("output/"+fname,wx.BITMAP_TYPE_PNG)
        
        
    def initColors(self):
        stampColors = []
        cols = []

        stampColors.append((wx.GREEN,wx.Colour(0,200,0)))
        cols.append('Green')
        stampColors.append((wx.RED,wx.Colour(200,0,0)))
        cols.append('Red')
        stampColors.append((wx.BLUE,wx.Colour(0,0,200)))
        cols.append('Blue')
        stampColors.append((wx.YELLOW,wx.Colour(200,200,0)))
        cols.append('Yellow')

        self.stampColors = stampColors
        self.colors = cols