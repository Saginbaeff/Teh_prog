from tkinter import *
import random
import math
import time
import collections
import _thread
from functools import partial


x_build = 100
y_build = 100
resources = collections.OrderedDict()
resources['Resources'] = '\n'
window = Tk()
window.title('Game')
window.geometry('1500x800+150+100')
window.grab_set()
background = PhotoImage(file='bg.gif', width=1200, height=800)
window_background = Canvas(window, width=1200, height=800)
window_background.create_image(600, 400, image=background)
window_background.create_image(600, 800, image=background)
resources_amount = Label(window, width=37, height=20, bg='gray85', fg='black', text='Resources:\n', font='Arial 10 bold')
resources_amount.place(x=1200, y=0)
hunters_hut_img = PhotoImage(file='hunters_hut.gif')
lumberjack_hut_img = PhotoImage(file='lumberjack_hut.gif')
miner_hut_img = PhotoImage(file='miner_hut.gif')
barrack_img = PhotoImage(file='barrack.gif')
stone = PhotoImage(file='stone.gif')
wood = PhotoImage(file='wood.gif')
food = PhotoImage(file='food.gif')
window_background.focus_set()
window_background.pack(expand=YES, fill=BOTH)


def construct(num):
    global buildings
    buildings[num][1][0] = buildings[num][1][1](x_build, y_build)
    if buildings[num][1][2] is not None:
        buildings[num][1][2]._building_to_collect = buildings[num][1][0]
    window_background.update()


def pack_building_buttons(e):
    for i in range(0, len(buildings) // 3):
        for j in range(0, 3):
            building_buttons.append(Button(window, width=12, height=3, bg='gray85', text=buildings[i * 3 + j][0],
                                           command=partial(construct, i * 3 + j)))
            building_buttons[i * 3 + j].place(x=1200 + j*94, y=386 + i * 60)
    i = len(buildings) // 3
    for j in range(0, len(buildings) % 3):
        building_buttons.append(Button(window, width=12, height=3, bg='gray85', text=buildings[i * 3 + j][0],
                                       command=partial(construct, i * 3 + j)))
        building_buttons[i * 3 + j].place(x=1200 + j * 94, y=386 + i * 60)


def set_coords(e):
    global x_build, y_build
    x_build = window.winfo_pointerx() - window.winfo_rootx()
    y_build = window.winfo_pointery() - window.winfo_rooty()


window_background.bind('<Button-3>', set_coords)


def singleton(cls):
    instances = {}

    def getinstance(*args):
        if cls not in instances or instances[cls]._deleted:
            instances[cls] = cls(*args)
        else:
            error = Tk()
            error.title('Error')
            error.geometry('300x40+800+350')
            error_desc = Text(error)
            error_desc.insert(1.0, instances[cls]._name + " already exists!")
            error_desc.pack()
            #error.mainloop()
            # to run tests without GUI
        return instances[cls]
    return getinstance


class Resource:
    def __init__(self, name, btc, img, x, y):
        self._building_to_collect = btc
        self._name = name
        self._x_coord = x
        self._y_coord = y
        self._image = img
        resources[self._name] = 0
        self._button = Button(image=img, bg='green')
        self._button.place(x=x, y=y)
        self._button.bind('<Button-3>', self._collect)

    def _unit_collect(self, unit):
        while True:
            unit._move(self._x_coord, self._y_coord, self._image.width(), self._image.height())
            ctr = 0
            while ctr < unit._capacity:
                ctr += unit._production
                time.sleep(5)
            unit._move(self._building_to_collect._x_coord, self._building_to_collect._y_coord, 50, 50)
            resources[self._name] += ctr
            time.sleep(1.5)
            resources_amount.configure(text='\n'.join('{}: {}'.format(key, val) for key, val in resources.items()))

    def _collect(self, e):
        if self._building_to_collect is not None:
            for i in self._building_to_collect._units:
                if (not i._dead) and (not i._now_working):
                    i._now_working = True
                    args = list()
                    args.append(i)
                    _thread.start_new(self._unit_collect, tuple(args))


class Building:
    def __init__(self, hp, x, y, properties, ut, img, nm):
        def _open_list(e):
            for i in range(0, len(self._props)):
                self._buttons[i].place(x=self._x_coord, y=self._y_coord + i * 26)

        self._hit_points = hp
        self._name = nm
        self._image = img
        self._main_button = Button(window, image=img, bg='green')
        self._unit_type = ut
        self._units = []
        self._buttons = []
        self._deleted = False
        self._x_coord = x
        self._y_coord = y
        self._props = properties
        self._main_button.bind("<Button-1>", _open_list)
        self._main_button.place(x=x, y=y)
        for i in range(0, len(self._props) - 1):
            self._buttons.append(Button(window, text=self._props[i], width=15, height=1, bg='grey', fg='black',
                                       command=partial(self._make_unit, self._unit_type[i])))
        self._buttons.append(Button(window, text=self._props[-1], width=15, height=1, bg='grey', fg='black',
                                   command=self._destroy))

    def _destroy(self):
        self._main_button.destroy()
        for i in self._buttons:
            i.destroy()
        for i in self._units:
            i.destroy()
        self._deleted = True

    def _make_unit(self, unit_type):
        u = unit_type(self._x_coord + random.choice([-15, self._image.width() + 45]) + random.randrange(-10, 10),
               self._y_coord + random.choice([-15, self._image.height() + 15]) + random.randrange(-10, 10))
        self._units.append(u)
        for i in self._buttons:
            i.place_forget()


class Unit:
    def __init__(self, hp, spd, x, y, clr, unit_name):
        self._x_coord = x
        self._y_coord = y
        self._hit_points = hp
        self._move_speed = spd
        self._point = window_background.create_oval(x, y, x+10, y+10, fill=clr, tag=unit_name)
        self._dead = False

    def _destroy(self):
        window_background.delete(self._point)
        self._dead = True

    def _move(self, x, y, delta_x, delta_y):
        while (self._x_coord - x) not in range(-self._move_speed - 1, self._move_speed + 1 + delta_x):
            window_background.move(self._point, math.copysign(self._move_speed, x - self._x_coord), 0)
            window_background.update()
            self._x_coord += math.copysign(self._move_speed, x - self._x_coord)
            time.sleep(0.1)
        while (self._y_coord - y) not in range(-self._move_speed - 1, self._move_speed + 1 + delta_y):
            window_background.move(self._point, 0, math.copysign(self._move_speed, y - self._y_coord))
            self._y_coord += math.copysign(self._move_speed, y - self._y_coord)
            window_background.update()
            time.sleep(0.1)


class Worker(Unit):
    def __init__(self, hp, spd, pr, cp, x, y, clr, unit_name):
        Unit.__init__(self, hp, spd, x, y, clr, unit_name)
        self._capacity = cp
        self._production = pr
        self._now_working = False


class Warrior(Unit):
    def __init__(self, hp, spd, dmg, x, y, clr, unit_name):
        Unit.__init__(self, hp, spd, x, y, clr, unit_name)
        self._damage = dmg


class Hunter(Worker):
    def __init__(self, x, y):
        Worker.__init__(self, 10, 10, 1, 3, x, y, 'brown', 'hunter')


class Lumberjack(Worker):
    def __init__(self, x, y):
        Worker.__init__(self, 10, 10, 1, 3, x, y, 'green', 'lumberjack')


class Miner(Worker):
    def __init__(self, x, y):
        Worker.__init__(self, 10, 10, 1, 3, x, y, 'grey', 'miner')


class Swordsman(Warrior):
    def __init__(self, x, y):
        Warrior.__init__(self, 30, 7, 10, x, y, 'snow3', 'swordsman')


class Archer(Warrior):
    def __init__(self, x, y):
        Warrior.__init__(self, 20, 12, 7, x, y, 'OliveDrab4', 'archer')


class Horseman(Warrior):
    def __init__(self, x, y):
        Warrior.__init__(self, 40, 20, 15, x, y, 'gold2', 'horseman')


@singleton
class HuntersHut(Building):
    def __init__(self, x, y):
        Building.__init__(self, 30, x, y, ['New Hunter', 'Destroy'], [Hunter], hunters_hut_img, 'Hunters Hut')


@singleton
class LumberjackHut(Building):
    def __init__(self, x, y):
        Building.__init__(self, 30, x, y, ['New Lumberjack', 'Destroy'], [Lumberjack], lumberjack_hut_img, 'Lumberjack Hut')


@singleton
class MinerHut(Building):
    def __init__(self, x, y):
        Building.__init__(self, 30, x, y, ['New Miner', 'Destroy'], [Miner], miner_hut_img, 'Miner Hut')


@singleton
class Barrack(Building):
    def __init__(self, x, y):
        Building.__init__(self, 100, x, y, ['New Swordsman', 'New Archer', 'New Horseman', 'Destroy'],
                          [Swordsman, Archer, Horseman], barrack_img, 'Barrack')


stone_res = Resource('Stone', None, stone, random.randrange(100, 1000), random.randrange(100, 500))
wood_res = Resource('Wood', None, wood, random.randrange(100, 1000), random.randrange(100, 500))
food_res = Resource('Food', None, food, random.randrange(100, 1000), random.randrange(100, 500))
buildings = [['Hunters Hut', [None, HuntersHut, food_res]], ['Lumberjack Hut', [None, LumberjackHut, wood_res]],
             ['Miner Hut', [None, MinerHut, stone_res]], ['Barrack', [None, Barrack, None]]]
building_buttons = []
create_building = Button(window, width=12, height=3, bg='gray85', text='Create Building')
create_building.bind('<Button-1>', pack_building_buttons)
create_building.place(x=1200, y=326)

#window.mainloop()
#to run tests without GUI


