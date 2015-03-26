import wx

class MyPanel(wx.Panel):
    def __init__(self, parent, id):
        # create a panel
        wx.Panel.__init__(self, parent, id)
        self.SetBackgroundColour("white")
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        self.dc = wx.PaintDC(self)
        self.dc.BeginDrawing()
        self.dc.SetPen(wx.Pen("grey",style=wx.TRANSPARENT))
        self.dc.SetBrush(wx.Brush("grey", wx.SOLID))
        # set x, y, w, h for rectangle
        self.dc.DrawRectangle(250,250,50, 50)
        self.dc.EndDrawing()
        del self.dc

app = wx.PySimpleApp()
frame = wx.Frame(None, -1, "Live Game", size = (500, 500))
MyPanel(frame,-1)
frame.Show(True)
app.MainLoop()