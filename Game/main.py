import tkinter as tk
import random
import math
import time
import collections
from functools import partial
import _thread


X_BUILD = 100
Y_BUILD = 100
RESOURCES = collections.OrderedDict()
RESOURCES['Resources'] = '\n'
WINDOW = tk.Tk()
WINDOW.title('Game')
WINDOW.geometry('1500x800+150+100')
WINDOW.grab_set()
BACKGROUND = tk.PhotoImage(file='bg.gif', width=1200, height=800)
WINDOW_BACKGROUND = tk.Canvas(WINDOW, width=1200, height=800)
WINDOW_BACKGROUND.create_image(600, 400, image=BACKGROUND)
WINDOW_BACKGROUND.create_image(600, 800, image=BACKGROUND)
RESOURCES_AMOUNT = tk.Label(WINDOW, width=37, height=20, bg='gray85', fg='black', text='Resources:\n', font='Arial 10 bold')
RESOURCES_AMOUNT.place(x=1200, y=0)
HUNTERS_HUT_IMG = tk.PhotoImage(file='hunters_hut.gif')
LUMBERJACK_HUT_IMG = tk.PhotoImage(file='lumberjack_hut.gif')
MINER_HUT_IMG = tk.PhotoImage(file='miner_hut.gif')
BARRACK_IMG = tk.PhotoImage(file='barrack.gif')
STONE = tk.PhotoImage(file='stone.gif')
WOOD = tk.PhotoImage(file='wood.gif')
FOOD = tk.PhotoImage(file='food.gif')
WINDOW_BACKGROUND.focus_set()
WINDOW_BACKGROUND.pack(expand=tk.YES, fill=tk.BOTH)


class BarrackRequestHandler:
    def __init__(self, successor):
        self.successor = successor

    def handle(self, *args):
        # do something
        return None

    def error_message(self, msg):
        error = tk.Tk()
        error.title('Error')
        error.geometry('300x40+800+350')
        error_desc = tk.Text(error)
        error_desc.insert(1.0, msg)
        error_desc.pack()
        #error.mainloop()

    def unpack(self):
        for i in BUILDINGS[3][1][0].division_buttons:
            i.place_forget()
        BUILDINGS[3][1][0].division_buttons = list()


class PlaceButtonsHandler(BarrackRequestHandler):
    def handle(self, *args):
        if BUILDINGS[3][1][0] is not None:
            BUILDINGS[3][1][0].place_division_buttons(self.successor, *args)
        else:
            self.error_message('Barrack does not exist!')


class DivisionMoveHandler(BarrackRequestHandler):
    def handle(self, *args):
        self.unpack()
        if BUILDINGS[3][1][0].DIVISIONS[args[0]][1][0][args[1]].get_size() == 0:
            self.error_message(BUILDINGS[3][1][0].DIVISIONS[args[0]][0] + ' is empty!')
        else:
            self.successor(*args)


class AddUnitHandler(BarrackRequestHandler):
    def handle(self, *args):
        self.unpack()
        if BUILDINGS[3][1][0].DIVISIONS[args[0]][1][0][args[1]].get_size() >= BUILDINGS[3][1][0].DIVISIONS[args[0]][1][0][args[1]].capacity:
            del BUILDINGS[3][1][0].units[-1]
            self.error_message(BUILDINGS[3][1][0].DIVISIONS[args[0]][0] + ' is full!')
        else:
            self.successor(*args)


class HealDivisionHandler(BarrackRequestHandler):
    def handle(self, *args):
        self.unpack()
        if isinstance(BUILDINGS[3][1][0].DIVISIONS[args[0]][1][0][args[1]], AdditionalAbilities):
            self.successor(*args)
        else:
            self.error_message(BUILDINGS[3][1][0].DIVISIONS[args[0]][0] + 'is not upgraded!')


class UpgradeDivisionHandler(BarrackRequestHandler):
    def handle(self, *args):
        self.unpack()
        if isinstance(BUILDINGS[3][1][0].DIVISIONS[args[0]][1][0][args[1]], AdditionalAbilities):
            self.successor(*args)
        else:
            self.error_message(BUILDINGS[3][1][0].DIVISIONS[args[0]][0] + 'is already upgraded!')


def construct(num):
    global BUILDINGS
    BUILDINGS[num][1][0] = BUILDINGS[num][1][1](X_BUILD, Y_BUILD)
    if BUILDINGS[num][1][2] is not None:
        BUILDINGS[num][1][2].building_to_collect = BUILDINGS[num][1][0]
    WINDOW_BACKGROUND.update()
    for i in SIDE_BUTTONS[0]:
        i.place_forget()


def choose_squad():
    for i in range(0, len(BUILDINGS[3][1][0].DIVISIONS[1][1][0])):
        BUILDINGS[3][1][0].division_buttons.append(tk.Button(WINDOW, text=BUILDINGS[3][1][0].DIVISIONS[1][0] + ' ' + str(i + 1), width=15,
                                               height=1, bg='grey', fg='black', command=partial(choose_army, i)))

    for i in range(0, len(BUILDINGS[3][1][0].division_buttons)):
        BUILDINGS[3][1][0].division_buttons[i].place(x=BUILDINGS[3][1][0].x_coord, y=BUILDINGS[3][1][0].y_coord + i * 26)


def choose_army(squad_key):
    for i in BUILDINGS[3][1][0].division_buttons:
        i.place_forget()
    BUILDINGS[3][1][0].division_buttons = list()
    for i in range(0, len(BUILDINGS[3][1][0].DIVISIONS[0][1][0])):
        BUILDINGS[3][1][0].division_buttons.append(tk.Button(WINDOW, text=BUILDINGS[3][1][0].DIVISIONS[0][0] + ' ' + str(i + 1), width=15,
                                               height=1, bg='grey', fg='black', command=partial(BUILDINGS[3][1][0].add_squad_to_army, i, squad_key)))

    for i in range(0, len(BUILDINGS[3][1][0].division_buttons)):
        BUILDINGS[3][1][0].division_buttons[i].place(x=BUILDINGS[3][1][0].x_coord, y=BUILDINGS[3][1][0].y_coord + i * 26)


def new_division(num):
    BUILDINGS[3][1][0].DIVISIONS[num][1][0].append(BUILDINGS[3][1][0].DIVISIONS[num][1][1]())
    BARBARIANS.subscribe(BUILDINGS[3][1][0].DIVISIONS[num][1][0][-1])
    for i in SIDE_BUTTONS[1]:
        i.place_forget()


def pack_side_buttons(buttons, func, key):
    for i in range(0, len(buttons) // 3):
        for j in range(0, 3):
            SIDE_BUTTONS[key].append(tk.Button(WINDOW, width=12, height=3, bg='gray85', text=buttons[i * 3 + j][0], command=partial(func, i * 3 + j)))
            SIDE_BUTTONS[key][i * 3 + j].place(x=1200 + j * 94, y=386 + i * 60)
    i = len(buttons) // 3
    for j in range(0, len(buttons) % 3):
        SIDE_BUTTONS[key].append(tk.Button(WINDOW, width=12, height=3, bg='gray85', text=buttons[i * 3 + j][0], command=partial(func, i * 3 + j)))
        SIDE_BUTTONS[key][i * 3 + j].place(x=1200 + j * 94, y=386 + i * 60)


def set_coordinates():
    global X_BUILD, Y_BUILD
    X_BUILD = WINDOW.winfo_pointerx() - WINDOW.winfo_rootx()
    Y_BUILD = WINDOW.winfo_pointery() - WINDOW.winfo_rooty()


WINDOW_BACKGROUND.bind('<Button-3>', lambda event: set_coordinates())
WINDOW_BACKGROUND.bind('m', lambda event: PlaceButtonsHandler(DivisionMoveHandler(BUILDINGS[3][1][0].move_division).handle).handle(X_BUILD, Y_BUILD))
WINDOW_BACKGROUND.bind('h', lambda event: PlaceButtonsHandler(HealDivisionHandler(BUILDINGS[3][1][0].heal_division).handle).handle(BUILDINGS[3][1][0].x_coord, BUILDINGS[3][1][0].y_coord))
WINDOW_BACKGROUND.bind('u', lambda event: PlaceButtonsHandler(UpgradeDivisionHandler(BUILDINGS[3][1][0].upgrade_division).handle).handle(BUILDINGS[3][1][0].x_coord, BUILDINGS[3][1][0].y_coord))
WINDOW_BACKGROUND.bind('g', lambda event: choose_squad())


class Squad:
    def __init__(self):
        self.units = list()
        self.capacity = 10
        self.in_action = False
        self.state = InspiredState()

    def add_unit(self, unit):
        self.units.append(unit)

    def move(self, x_coordinate, y_coordinate, delta_x, delta_y):
        self.state.move(self.units, x_coordinate, y_coordinate, delta_x, delta_y)

    def __getattr__(self, item):
        if item == 'hit_points':
            result = 0
            for i in self.units:
                result += i.hit_points
            return result
        elif item == 'damage':
            return self.sum_damage()
        elif item == 'max_hit_points':
            result = 0
            for i in self.units:
                result += i.max_hit_points
            return result

    def get_size(self):
        return len(self.units)

    def sum_damage(self):
        damage = 0
        for i in range(0, len(self.units)):
            if not self.units[i].dead:
                damage += self.units[i].damage
        return damage

    def get_damage(self, damage):
        self.state.get_damage(damage, self.units)
        if self.max_hit_points / 4 < self.hit_points < self.max_hit_points / 1.5:
            self.state = NormalState()
        elif self.max_hit_points / 4 > self.hit_points:
            self.state = LowState()

    def receive_notification(self, x_coordinate, y_coordinate):
        _thread.start_new(self.defend, (x_coordinate, y_coordinate))

    def defend(self, x_coordinate, y_coordinate):
        self.state.defend(x_coordinate, y_coordinate, self.move, self.sum_damage)


class Army(Squad):
    def __init__(self):
        super().__init__()
        self.capacity = 100

    def get_size(self):
        result = 0
        for i in range(0, len(self.units)):
            if hasattr(self.units[i], '__iter__'):
                result += self.units[i].get_size()
            else:
                result += 1
        return result


class SquadState:
    def get_damage(self, damage, units):
        #do_something
        return None

    def move(self, units, x_coordinate, y_coordinate, delta_x, delta_y):
        #do_something
        return None

    def defend(self,  x_coordinate, y_coordinate, move, sum_damage):
        #do_something
        return None


class InspiredState(SquadState):
    def get_damage(self, damage, units):
        for i in units:
            if i.hit_points > damage / 2:
                i.hit_points -= damage / 2

    def move(self,  units, x_coordinate, y_coordinate, delta_x, delta_y):
        for i in units:
            _thread.start_new(i.move, (x_coordinate, y_coordinate, delta_x, delta_y))

    def defend(self, x_coordinate, y_coordinate, move, sum_damage):
        move(x_coordinate, y_coordinate, 10, 10)
        while BARBARIANS.army.get_size() > 0:
            BARBARIANS.army.get_damage(sum_damage() * 2)
            time.sleep(1)


class NormalState(SquadState):
    def get_damage(self, damage, units):
        units[-1].hit_points -= damage
        if units[-1].hit_points < 0:
            del units[-1]
            units.pop()
        WINDOW_BACKGROUND.update()

    def move(self,  units, x_coordinate, y_coordinate, delta_x, delta_y):
        time.sleep(1.0)
        for i in units:
            _thread.start_new(i.move, (x_coordinate, y_coordinate, delta_x, delta_y))

    def defend(self, x_coordinate, y_coordinate, move, sum_damage):
        move(x_coordinate, y_coordinate, 10, 10)
        while BARBARIANS.army.get_size() > 0:
            BARBARIANS.army.get_damage(sum_damage())
            time.sleep(2.0)


class LowState(SquadState):
    def get_damage(self, damage, units):
        units[-1].hit_points -= damage * 2
        if units[-1].hit_points < 0:
            del units[-1]
            units.pop()
        WINDOW_BACKGROUND.update()
        for i in units:
            _thread.start_new(i.move, (BUILDINGS[3][1][0].x_coord, BUILDINGS[3][1][0].y_coord, BUILDINGS[3][1][0].image.width(), BUILDINGS[3][1][0].image.height()))

    def move(self,  units, x_coordinate, y_coordinate, delta_x, delta_y):
        time.sleep(5.0)
        for i in units:
            _thread.start_new(i.move, (x_coordinate, y_coordinate, delta_x, delta_y))

    def defend(self, x_coordinate, y_coordinate, move, sum_damage):
        #do_nothing
        return None


class AdditionalAbilities(Army):
    def __init__(self, division):
        super().__init__()
        self.units = division.units
        self.in_action = division.in_action
        if isinstance(division, Squad):
            self.capacity = 10
        else:
            self.capacity = 100

    def healing(self):
        for i in self.units:
            if i.hit_points < i.max_hit_points:
                i.hit_points += 1
        time.sleep(1)


def singleton(cls):
    instances = {}

    def get_instance(*args):
        if cls not in instances or instances[cls].deleted:
            instances[cls] = cls(*args)
        else:
            error = tk.Tk()
            error.title('Error')
            error.geometry('300x40+800+350')
            error_desc = tk.Text(error)
            error_desc.insert(1.0, instances[cls].name + " already exists!")
            error_desc.pack()
            #error.mainloop()
        return instances[cls]
    return get_instance


class Resource:
    def __init__(self, name, btc, img, x, y):
        self.building_to_collect = btc
        self.name = name
        self.x_coord = x
        self.y_coord = y
        self.image = img
        RESOURCES[self.name] = 0
        self.button = tk.Button(image=img, bg='green')
        self.button.place(x=x, y=y)
        self.button.bind('<Button-3>', lambda event: self.collect())

    def unit_collect(self, unit):
        while True:
            unit.move(self.x_coord, self.y_coord, self.image.width(), self.image.height())
            ctr = 0
            while ctr < unit.capacity:
                ctr += unit.production
                time.sleep(5)
            unit.move(self.building_to_collect.x_coord, self.building_to_collect.y_coord, 50, 50)
            RESOURCES[self.name] += ctr
            time.sleep(1.5)
            RESOURCES_AMOUNT.configure(text='\n'.join('{}: {}'.format(key, val) for key, val in RESOURCES.items()))

    def collect(self, ):
        if self.building_to_collect is not None:
            for i in self.building_to_collect.units:
                if (not i.dead) and (not i.now_working):
                    i.now_working = True
                    args = list()
                    args.append(i)
                    _thread.start_new(self.unit_collect, tuple(args))


class Building:
    def __init__(self, hp, x, y, properties, ut, img, nm):
        def open_list():
            for i in range(0, len(self.props)):
                self.buttons[i].place(x=self.x_coord, y=self.y_coord + i * 26)

        self.hit_points = hp
        self.name = nm
        self.image = img
        self.main_button = tk.Button(WINDOW, image=img, bg='green')
        self.unit_type = ut
        self.units = []
        self.buttons = []
        self.deleted = False
        self.x_coord = x
        self.y_coord = y
        self.props = properties
        self.main_button.bind("<Button-1>", lambda event: open_list())
        self.main_button.place(x=x, y=y)
        for i in range(0, len(self.props) - 1):
            self.buttons.append(tk.Button(WINDOW, text=self.props[i], width=15, height=1, bg='grey', fg='black',
                                          command=partial(self.make_unit, self.unit_type[i])))
        self.buttons.append(tk.Button(WINDOW, text=self.props[-1], width=15, height=1, bg='grey', fg='black',
                                      command=self.destroy))

    def destroy(self):
        self.main_button.destroy()
        for i in self.buttons:
            i.destroy()
        for i in self.units:
            i.destroy()
        self.deleted = True

    def make_unit(self, unit_type):
        new_unit = unit_type(self.x_coord + random.choice([-15, self.image.width() + 45]) + random.randrange(-10, 10),
                             self.y_coord + random.choice([-15, self.image.height() + 15]) + random.randrange(-10, 10))
        self.units.append(new_unit)
        for i in self.buttons:
            i.place_forget()


class Unit:
    def __init__(self, hp, spd, x, y, clr, unit_name):
        self.x_coord = x
        self.y_coord = y
        self.hit_points = hp
        self.max_hit_points = hp
        self.move_speed = spd
        self.point = WINDOW_BACKGROUND.create_oval(x, y, x + 10, y + 10, fill=clr, tag=unit_name)
        self.dead = False

    def __del__(self):
        WINDOW_BACKGROUND.delete(self.point)

    def destroy(self):
        WINDOW_BACKGROUND.delete(self.point)
        self.dead = True

    def move(self, x_coordinate, y_coordinate, delta_x, delta_y):
        while (self.x_coord - x_coordinate) not in range(-self.move_speed - 1, self.move_speed + 1 + delta_x):
            WINDOW_BACKGROUND.move(self.point, math.copysign(self.move_speed, x_coordinate - self.x_coord), 0)
            WINDOW_BACKGROUND.update()
            self.x_coord += math.copysign(self.move_speed, x_coordinate - self.x_coord)
            time.sleep(0.1)
        while (self.y_coord - y_coordinate) not in range(-self.move_speed - 1, self.move_speed + 1 + delta_y):
            WINDOW_BACKGROUND.move(self.point, 0, math.copysign(self.move_speed, y_coordinate - self.y_coord))
            self.y_coord += math.copysign(self.move_speed, y_coordinate - self.y_coord)
            WINDOW_BACKGROUND.update()
            time.sleep(0.1)


class Worker(Unit):
    def __init__(self, hp, spd, pr, cp, x, y, clr, unit_name):
        Unit.__init__(self, hp, spd, x, y, clr, unit_name)
        self.capacity = cp
        self.production = pr
        self.now_working = False


class Warrior(Unit):
    def __init__(self, hp, spd, dmg, x, y, clr, unit_name):
        Unit.__init__(self, hp, spd, x, y, clr, unit_name)
        self.damage = dmg


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


class Barbarian(Warrior):
    def __init__(self, x, y):
        Warrior.__init__(self, 30, 15, 7, x, y, 'red', 'barbarian')


@singleton
class HuntersHut(Building):
    def __init__(self, x, y):
        Building.__init__(self, 30, x, y, ['New Hunter', 'Destroy'], [Hunter], HUNTERS_HUT_IMG, 'Hunters Hut')


@singleton
class LumberjackHut(Building):
    def __init__(self, x, y):
        Building.__init__(self, 30, x, y, ['New Lumberjack', 'Destroy'], [Lumberjack], LUMBERJACK_HUT_IMG, 'Lumberjack Hut')


@singleton
class MinerHut(Building):
    def __init__(self, x, y):
        Building.__init__(self, 30, x, y, ['New Miner', 'Destroy'], [Miner], MINER_HUT_IMG, 'Miner Hut')


@singleton
class Barrack(Building):
    def __init__(self, x, y):
        Building.__init__(self, 100, x, y, ['New Swordsman', 'New Archer', 'New Horseman', 'Destroy'],
                          [Swordsman, Archer, Horseman], BARRACK_IMG, 'Barrack')
        self.division_buttons = list()
        self.ARMIES = list()
        self.SQUADS = list()
        self.DIVISIONS = [['Army', [self.ARMIES, Army]], ['Squad', [self.SQUADS, Squad]]]
        create_division = tk.Button(WINDOW, width=12, height=3, bg='gray85', text='Create Division',
                                    command=partial(pack_side_buttons, self.DIVISIONS, new_division, 1))
        create_division.place(x=1294, y=326)

    def place_division_buttons(self, func, x_coordinate, y_coordinate):
        for j in range(0, 2):
            for i in range(0, len(self.DIVISIONS[j][1][0])):
                self.division_buttons.append(tk.Button(WINDOW, text=self.DIVISIONS[j][0] + ' ' + str(i + 1), width=15,
                                                       height=1, bg='grey', fg='black', command=partial(func, j, i)))
        for i in range(0, len(self.division_buttons)):
            self.division_buttons[i].place(x=x_coordinate, y=y_coordinate + i * 26)

    def add_unit_to_division(self, division_type, key):
        self.DIVISIONS[division_type][1][0][key].add_unit(self.units[-1])

    def add_squad_to_army(self, army_key, squad_key):
        for i in BUILDINGS[3][1][0].division_buttons:
            i.place_forget()
        BUILDINGS[3][1][0].division_buttons = list()
        self.DIVISIONS[0][1][0][army_key].add_unit(self.DIVISIONS[1][1][0][squad_key])

    def make_unit(self, unit_type):
        PlaceButtonsHandler(AddUnitHandler(self.add_unit_to_division).handle).handle(self.x_coord, self.y_coord)
        super().make_unit(unit_type)

    def move_division(self, division_type, key):
        self.DIVISIONS[division_type][1][0][key].move(X_BUILD, Y_BUILD, 20, 20)

    def upgrade_division(self, division_type, key):
        self.DIVISIONS[division_type][1][0][key] = AdditionalAbilities(self.DIVISIONS[division_type][1][0][key])

    def heal_army(self, division_type, key):
        self.DIVISIONS[division_type][1][0][key].healing()


class Enemy:
    def __init__(self):
        self.army = Army()
        self.subscribers = list()

    def spawn_enemies(self, quantity=5, x_coordinate=100, y_coordinate=100):
        for i in range(0, quantity):
            self.army.add_unit(Barbarian(x_coordinate + random.choice([-15, 15]) + random.randrange(-10, 10),
                                         y_coordinate + random.choice([-15, 15]) + random.randrange(-10, 10)))
            WINDOW.update()

    def subscribe(self, obj):
        self.subscribers.append(obj)

    def attack_notify(self, x_coordinate=100, y_coordinate=100):
        for i in self.subscribers:
            i.receive_notification(x_coordinate, y_coordinate)

    def start_invasion(self):
        self.spawn_enemies()
        self.attack_notify()

    def activate(self):
        if random.choice([True, False]):
            self.start_invasion()
        WINDOW.after(60000, BARBARIANS.activate)


BARBARIANS = Enemy()
STONE_RES = Resource('Stone', None, STONE, random.randrange(100, 1000), random.randrange(100, 500))
WOOD_RES = Resource('Wood', None, WOOD, random.randrange(100, 1000), random.randrange(100, 500))
FOOD_RES = Resource('Food', None, FOOD, random.randrange(100, 1000), random.randrange(100, 500))
BUILDINGS = [['Hunters Hut', [None, HuntersHut, FOOD_RES]], ['Lumberjack Hut', [None, LumberjackHut, WOOD_RES]],
             ['Miner Hut', [None, MinerHut, STONE_RES]], ['Barrack', [None, Barrack, None]]]
SIDE_BUTTONS = [[], []]
CREATE_BUILDING = tk.Button(WINDOW, width=12, height=3, bg='gray85', text='Create Building',
                            command=partial(pack_side_buttons, BUILDINGS, construct, 0))
CREATE_BUILDING.place(x=1200, y=326)
WINDOW.after(10000, BARBARIANS.activate)
#WINDOW.mainloop()
