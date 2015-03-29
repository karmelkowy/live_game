# -*- coding: utf-8 -*-
import wx, random, time

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
    child_age = 10
    old_age = 5
    def __init__(self, pos=(0,0), sex="man"):
        self.pos = pos
        self.sex = sex
        self.can_multiply = False
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
        if self.age < self.child_age:
            color = "PINK"
        elif self.age >= self.child_age and self.age < self.dead_age - self.old_age:
            self.can_multiply = True
            if self.sex == "man":
                color = "RED"
            else:
                color = "GREEN"

        elif self.age >= self.dead_age - self.old_age:
            self.can_multiply = False
            color = "GREY"



        dc.SetPen(wx.Pen(color, 1))
        dc.SetBrush(wx.Brush(color, wx.SOLID))
        dc.DrawRectangle(x, y, self.s, self.s)

    def getNextPos(self):
        return self.directions_map[self.dir]

    def __repr__(self):
        return '%s: pos=%s' % (self.name, str(self.pos) )

    
class Map2d:
    def __init__(self):
        self.obiekty = []
        self.mapa = {}
        self.born_ratio_map = {}

    def Add(self, obj, instant=False):
        if not self.Colision(obj.pos, obj):
            self.obiekty.append(obj)
        elif instant:
            self.obiekty.append(obj)

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
        wx.Frame.__init__( self, None, title="Gra w życie")
        
        self.s = size
        # określenie wymierów mapy
        self.w, self.h = 1200/self.s, 600/self.s

        self.tools = ['man', 'woman', 'rubber']
        self.left_tool = self.tools[0]
        self.right_tool = self.tools[2]

        self.absolute_live_time = 0
        self.born_ratio = 0


        # dodowanie layoutu
        main_panel = wx.Panel(self, wx.ID_ANY)
        main_panel.SetFocus()

        box = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(main_panel, wx.ID_ANY, size=(self.w*self.s, self.h*self.s))
        box.Add(self.panel, 1, wx.EXPAND)

        button_box = wx.BoxSizer(wx.HORIZONTAL)

        stop_play_button = wx.Button(main_panel, -1, 'Stop')
        button_box.Add(stop_play_button, 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.playStop, stop_play_button)

        for tool in self.tools:
            tool_btn = wx.Button(main_panel, -1, tool)
            button_box.Add(tool_btn, 1, wx.EXPAND)
            self.Bind(wx.EVT_BUTTON, self.toolChange, tool_btn)

        box.Add(button_box, 0)

        main_panel.SetSizer(box)


        # bindowanie eventów
        self.panel.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)

        main_panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        self.panel.Bind( wx.EVT_PAINT, self.OnPaint )

        self.timer = wx.Timer(self)
        self.timer.Start(5)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        # aby zmienić prędkość
        #self.timer.Stop()
        #self.timer.Start(100)

        self.SetSize((self.w*self.s, self.h*self.s+50))
        self.Refresh()
        self.Centre()


        self.map = Map2d()

        for n in range(20):
            pos = (n,n)
            self.spawn(pos, "woman")

        for n in range(20):
            pos = (self.w-n,self.h-n)
            self.spawn(pos, "man")



    def toolChange(self, evt):
        self.left_tool = evt.GetEventObject().GetLabel()

    def playStop(self, evt):
        button = evt.GetEventObject()
        if self.timer.IsRunning():
            self.timer.Stop()
            button.SetLabel("Start")
        else:
            button.SetLabel("Stop")
            self.timer.Start()

    def rubber(self, pos):
        rub_size = 50
        for x in range(rub_size):
            for y in range(rub_size):
                new_pos = pos[0]+x-rub_size/2, pos[1]+y-rub_size/2
                obj_list = self.map.mapa.get(new_pos, None)
                if obj_list is not None:
                    for obj in obj_list:
                        self.map.obiekty.remove(obj)
                        del obj


    def reCountBornMap(self):
        #{grid:[n_dzieci, n_dorosłych]}
        # {(0,0):[3,2]}
        map = {}
        for obj in self.map.obiekty:
            x, y = obj.pos
            grid = x/10, y/10
            n_child, n_parnt = map.get(grid, (0, 0))
            if obj.age < 10:
                n_child += 1
            elif obj.can_multiply:
                n_parnt +=1
            map[grid] = n_child, n_parnt

        self.born_ratio_map = {}
        self.grid_to_clear = []
        for grid, values in map.iteritems():
            n_child, n_parnt = values
            if n_parnt+n_child > 20:
                self.grid_to_clear.append(grid)

            parents = n_child+n_parnt
            if parents > 0:
                ratio = float(n_child)/(parents)
            else:
                ratio = 0
            self.born_ratio_map[grid] = ratio


    def spawn(self, pos, sex, instant=False, age=0):
        obj = Object2d()
        obj.pos = (pos[0],pos[1])
        obj.sex = sex
        obj.age = age
        self.map.Add(obj, instant)

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

            obj_list = self.map.mapa[new_pos]
            colision_obj = obj_list[0]
            if obj.sex != colision_obj.sex and obj.can_multiply and colision_obj.can_multiply:
                obj.ChooseDirection()
                colision_obj.ChooseDirection()

                #self.map.CreateColisionMap()
                #self.reCountBornMap()

                grid = (new_pos[0]/10, new_pos[1]/10)
                ratio = self.born_ratio_map[grid]
                ratio = int((1 - ratio) * 100)
                born_chance = random.randint(80, 100)

                if born_chance < ratio:
                    child_sex = random.choice(('man', 'woman'))
                    self.spawn(new_pos, child_sex, True)
            else:
                # zmiana kierunku w przypadku kolizji z tym samym kolorem
                obj.ChooseDirection()

        else:
            # zrobienie kroku
            obj.pos = new_pos

        # przeliczenie mapy kolizji
        #self.map.CreateColisionMap()

    def OnMouse(self,event):
        self.mouse_pos = event.GetPosition()
        x, y = self.mouse_pos
        x /= self.s
        y /= self.s
        pos = x, y
        self.map.CreateColisionMap()
        tool_size = 10
        if event.LeftIsDown():
            if self.left_tool == self.tools[0] or self.left_tool == self.tools[1]:
                for x in range(tool_size):
                    for y in range(tool_size):
                        if random.randint(0, 30) == 0:
                            new_pos = pos[0]-tool_size/2+x, pos[1]-tool_size/2+y
                            self.spawn(new_pos, self.left_tool, age=11)
            elif self.left_tool == 'rubber':
                self.rubber(pos)

        if event.RightIsDown():
            if self.right_tool == self.tools[0] or self.right_tool == self.tools[1]:
                self.spawn(pos, self.right_tool)
            elif self.right_tool == 'rubber':
                self.rubber(pos)
        self.Refresh()

    def OnTimer(self, event):
        self.timer.Stop()
        start = time.time()
        self.reCountBornMap()
        self.map.CreateColisionMap()



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
            obj_to_del = False
            if obj.age > obj.dead_age:
                obj_to_del = True

            for grid in self.grid_to_clear:
                x, y = grid[0]*10, grid[1]*10
                obj_x, obj_y = obj.pos
                rand = random.randint(0, 10)
                if (obj_x > x and obj_x < x + 10) and (obj_y > y and obj_y < y + 10) and rand == 0:
                    #obj.dead_age = obj.age + random.randint(5, 8)
                    obj_to_del = True

            if obj_to_del:
                self.map.obiekty.remove(obj)
                del obj

        # odświerzenie panelu rysującego ( wykonanie def OnPaint )
        self.Refresh()
        self.absolute_live_time += 1
        self.time_of_cykl = time.time() - start
        self.timer.Start()



    def OnKeyPress(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            exit()            

    def OnPaint(self, event):
        self.reCountBornMap()

        dc = wx.PaintDC(self.panel)
        dc.Clear()
        self.map.Draw(dc)
        '''
        for grid, ratio in self.born_ratio_map.iteritems():
            ratio = int((1 - ratio) * 10)
            x, y = grid[0]*10*self.s, grid[1]*10*self.s
            dc.DrawText(str(ratio), x, y)
        '''
        for grid in self.grid_to_clear:
            x, y = grid[0]*10*self.s, grid[1]*10*self.s
            dc.DrawText("clear", x, y)

        n_child = 0
        n_man = 0
        n_woman = 0
        n_grandpa = 0
        sum_wieku = 0
        for obj in self.map.obiekty:
            sum_wieku += obj.age
            if obj.age < obj.child_age:
                n_child += 1
            elif obj.age >= obj.child_age and obj.age < obj.dead_age - 5:
                if obj.sex == "man":
                    n_man += 1
                else:
                    n_woman += 1
            elif obj.age >= obj.dead_age - obj.old_age:
                n_grandpa += 1

        sum_populacji = n_child + n_man + n_woman + n_grandpa + 0.1

        print 3*"\n"

        print "cykl zegara: %d  , czas cyklu: %f" % (self.absolute_live_time, self.time_of_cykl)
        print "dzieci: %d\nkobiet: %d\nmężczyzn: %d\ndziadków: %d" % (n_child, n_woman, n_man, n_grandpa)
        print "w sumie: %d" % (sum_populacji)
        if sum_populacji > 0:
            print "srednia wieku: %d" % (sum_wieku/sum_populacji)
        else:
            print "srednia wieku: nikt nie żyje"

    def __repr__(self):
        return str(self.mapa)


app = wx.App(False)
frame = MyFrame()
frame.Show()
app.MainLoop()