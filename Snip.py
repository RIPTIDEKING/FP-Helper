import wx
import PIL
from EditImage import EditImageFrame

class SnipFrame(wx.Frame):

    def __init__(self, parent = None, title = ""):
        super().__init__(None,title = title,size = wx.DisplaySize())

        self.parent = parent
        self.Bind(wx.EVT_CLOSE,self.parent.onClose)
        self.panel = wx.Panel(self, size=self.GetSize())

        self.startPos = None
        self.endPos = None

        self.beginCapture = False

        self.panel.Bind(wx.EVT_LEFT_DOWN,self.startCapture)
        self.panel.Bind(wx.EVT_MOTION,self.dragMouse)
        self.panel.Bind(wx.EVT_LEFT_UP,self.endCapture)
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)

    def onInit(self):
        self.startPos = None
        self.endPos = None

        self.beginCapture = False
        self.parent.image_frame = EditImageFrame(self.parent,title='FP-Helper')

    def dragMouse(self,event):

        if event.Dragging() and event.LeftIsDown():
            self.endPos = event.GetPosition()
            self.Refresh()

    def startCapture(self,event):
        self.startPos = event.GetPosition()
        self.beginCapture = True

    def endCapture(self,event):
        self.endPos = event.GetPosition()
        self.grabScreenShot()
        # self.Destroy()

    def OnPaint(self, event):
        if not self.beginCapture: return

        dc = wx.PaintDC(self.panel)
        dc.SetPen(wx.Pen('green', 5))
        dc.SetBrush(wx.Brush(wx.Colour(0, 100, 0), wx.TRANSPARENT))

        dc.DrawRectangle(self.startPos.x, self.startPos.y, self.endPos.x - self.startPos.x, self.endPos.y - self.startPos.y)


    def grabScreenShot(self):
        self.SetTransparent(0)

        screenShot = PIL.ImageGrab.grab()
        screenShot = screenShot.crop((self.startPos.x,self.startPos.y,self.endPos.x,self.endPos.y))
        ssConvert = screenShot.convert('RGB')
        ssConvert = ssConvert.tobytes()

        ssImage = wx.Image(*screenShot.size)
        ssImage.SetData(ssConvert)
        ssImage = wx.Bitmap(ssImage)

        self.Hide()
        self.parent.image_frame.showImage(ssImage)
        # screenshot.save(savePath, 'PNG')   
        
