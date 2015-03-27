# -*- coding: utf-8 -*-
import wx, random

#zakres losowości długości życia
live = range(80, 110)
# wielkość pojedyńczego obiektu im większe tym mniej ich na ekranie
size = 5

class Object2d:
    s = size
    directions_map = {'RIGHT': (1, 0),
                      'DOWN': (0, 1),
                      'LEFT': (-1, 0),
                      'UP': (0, -1),
                      'RIGHT_UP': (1, -1),
                      'RIGHT_DOWN': (1, 1),
                      'LEFT_UP': (-1, -1),
                      'LEFT_DOWN': (-1, 1),
                      'STAY': (0, 0)}
    def __init__(self, pos=(0,0), name='unknown', color='BLACK', if_label=False, dead_age=0):
        self.pos = pos
        self.name = name
        self.color = color
        self.if_label = if_label
        self.dead_age = dead_age
        if self.dead_age == 0:
            self.dead_age = random.choice(live)

        self.age = 0
        self.dir = None
        self.ChooseDirection()

    def ChooseDirection(self):
        self.dir = random.choice(self.directions_map.keys())

    def Draw(self, dc):
        x, y = self.pos
        x = x*self.s
        y = y*self.s
        dc.SetPen(wx.Pen(self.color, 1))
        dc.SetBrush(wx.Brush(self.color, wx.SOLID))
        dc.DrawRectangle(x, y, self.s, self.s)
        dc.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
        dc.SetPen(wx.Pen(wx.NamedColour('black'), 20))

        if self.if_label:
            dc.DrawText(str(self.age),x,y)

    def getNextPos(self):
        return self.directions_map[self.dir]

    def __repr__(self):
        return '%s: pos=%s' % (self.name, str(self.pos) )

    
class Map2d:
    def __init__(self):
        self.obiekty = []
        self.mapa = {}

    def Add(self, obj2d):
        self.obiekty.append(obj2d)
        
    def GetName(self, pos):
        for obj in self.obiekty:
            if obj.pos == pos:
                return obj.name

    def Draw(self, dc):
        for obj in self.obiekty:
            obj.Draw(dc)
        
    def CreateColisionMap(self):
        self.mapa = {}
        for obj in self.obiekty:
            pos = obj.pos
            obj_list = self.mapa.get(pos, None) 
            if obj_list is None:
                self.mapa[pos] = [obj]
            else:
                obj_list.append(obj)
                self.mapa[pos] = obj_list
        
    def Colision(self, pos, self_obj):
        obj_list = self.mapa.get(pos, None)
        if obj_list is None:
            return False
        for obj in obj_list:
            if obj != self_obj:
                return True
 
        return False
            
    def __repr__(self):
        txt = ''
        for pos, obj_list in self.mapa.iteritems():
            txt += str(pos) + ': '
            for obj in obj_list:
                txt += obj.name + ', '
        return txt


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__( self, None, title="My First Game" )
        
        self.s = size
        # określenie wymierów mapy
        self.w, self.h = 600/self.s, 600/self.s

        # dudowanie layoutu
        main_panel = wx.Panel(self, wx.ID_ANY)
        main_panel.SetFocus()

        box = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(main_panel, wx.ID_ANY, size=(self.w*self.s, self.h*self.s))
        box.Add(self.panel, 1, wx.EXPAND)
        main_panel.SetSizer(box)

        # bindowanie eventów
        self.panel.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)

        main_panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        self.panel.Bind( wx.EVT_PAINT, self.OnPaint )

        self.timer = wx.Timer(self)
        self.timer.Start(200)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        # aby zmienić prędkość
        #self.timer.Stop()
        #self.timer.Start(100)

        self.SetSize((self.w*self.s, self.h*self.s))
        self.Refresh()
        self.Centre()

        self.map = Map2d()

        for n in range(20):
            man = Object2d()
            man.pos = (n,n)
            man.color = "GREEN"
            #man.if_label = True
            self.map.Add(man)

        for n in range(20):
            man = Object2d()
            man.pos = (self.w-n,self.h-n)
            man.color = "RED"
            #man.if_label = True
            self.map.Add(man)


    def Move(self, obj):
        # pobieranie obecnej pozycji
        x, y = obj.pos
        # pobieranie różnicy w pozycjach
        dif_x, dif_y = obj.getNextPos()

        # obliczanie przyszłych pozycji
        new_x = dif_x + x
        new_y = dif_y + y

        # opisanie wyjątków przy wyjściu za mape
        if (new_x < 0):
            new_x = 0
        elif (new_x > self.w-1):
            new_x = self.w-1

        if (new_y < 0):
            new_y = 0
        elif (new_y > self.h-1):
            new_y = self.h-1

        new_pos = (new_x, new_y)

        # sprawdzanie kolizji
        if self.map.Colision(new_pos, obj):
            #print "kolizja w (%d,%d)" % new_pos

            # zmiana kierunku w przypadku kolizji
            obj.ChooseDirection()

        else:
            # zrobienie kroku
            obj.pos = new_pos

        # przeliczenie mapy kolizji
        self.map.CreateColisionMap()

    def OnMouse(self,event):
        self.mouse_pos = event.GetPosition()
        x, y = self.mouse_pos
        x /= self.s
        y /= self.s
        pos = x, y
        if event.LeftIsDown():
            print "lewy (%dm,%d)" % pos
            man = Object2d()
            man.pos = (pos[0],pos[1])
            man.color = "RED"
            self.map.Add(man)


        if event.RightIsDown():
            print "prawy (%d,%d)" % pos
            man = Object2d()
            man.pos = (pos[0],pos[1])
            man.color = "GREEN"
            self.map.Add(man)

    def OnTimer(self, event):
        # dla każdego obiektu na mapie
        for obj in self.map.obiekty:
            # losowanie czy ma sie zmienić kierunek
            n = random.randint(0,3)
            if n == 0:
                # zmiana kierunku
                obj.ChooseDirection()
            # ruch obiektu
            self.Move(obj)
            # zwiększenie wieku
            obj.age += 1

            if obj.age >= obj.dead_age:
                self.map.obiekty.remove(obj)

                del obj
        # odświerzenie panelu rysującego ( wykonanie def OnPaint )
        self.Refresh()

    def OnKeyPress(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            exit()            

    def OnPaint( self, event):
        dc = wx.PaintDC(self.panel)
        dc.Clear()
        self.map.Draw(dc)

    def __repr__(self):
        return str(self.mapa)


app = wx.App(False)
frame = MyFrame()
frame.Show()
app.MainLoop()