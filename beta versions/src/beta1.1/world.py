import json
from debug import *
from accessor import *
from actions import ActionManager
import programs
import time
import image_manager
import file_manager
from subprocess import call
import display
import scenes
import sys
import random
random.seed()

"""
--------------------------
    World
--------------------------
Contains all the places in the world, all npcs, and the player. Is basically a container.
Can manipulate npcs and player to move around the world.
"""
class World:
    def __init__(self):

        self.running = True

        # initial load world data
        world_data = get_json('world_builder')
        
        # gameobjects
        self.gameobjects = GameObject.load(world_data['gameobjects'])
        self.computers = Computer.load(world_data['computers'])
        
        # locations
        self.locations = Location.load(world_data['locations'])
        
        # player
        self.player = Player.load(world_data['player'])
        
        self.time = Time.load(world_data['time'])
        
        # load npc's and their dialogues
        self.npcs = NPC.load(world_data['npcs'], all_dialogues())

        # load initial actions data
        self.action_manager = ActionManager.load(all_actions())

        self.worldstate = "normal"

    def update(self):
        self.player.talking = ""
        self.player.running = ""
        self.player.using = ""

        if self.time.now == "day":
            pass
        elif self.time.now == "night":
            pass

        if self.worldstate == "lose":
            scenes.lose()
            self.running = False
        elif self.worldstate == "win":
            scenes.end()
            # done! game is removed from saves since its finished
            finish_current_game()
            quit()

    def get_gameobject(self,name):
        if name in self.gameobjects:
            return self.gameobjects[name]
        return False

    def get_computer(self,name):
        if name in self.computers:
            return self.computers[name]
        return False

    def get_npc(self,name):
        if name in self.npcs:
            return self.npcs[name]
        return False

    def get_location(self,name):
        if name in self.locations:
            return self.locations[name]
        return False

    def save_gameobject(self, go):
        if go.name in self.gameobjects:
            self.gameobjects[go.name] = go
            return True
        return False

    def save_computer(self, comp):
        if comp.name in self.computers:
            self.computers[comp.name] = comp
            return True
        return False

    def save_npc(self, npc):
        if npc.name in self.npcs:
            self.npcs[npc.name] = npc
            return True
        return False

    def save_location(self, loc):
        if loc.name in self.locations:
            self.locations[loc.name] = loc
            return True
        return False

    def is_comp(self, name):
        for c in self.computers:
            if c.name == name:
                return True
        return False

    def is_go(self, name):
        for go in self.gameobjects:
            if go.name == name:
                return True
        return False


"""
--------------------------
    Location
--------------------------
Place in the world. In order to do certain actions, must be in a location
"""
class Location:
    def __init__(self, name, desc, connections, gameobjects, computers, day_npcs, night_npcs):
        self.name = name
        self.desc = desc
        self.connections = connections
        self.gameobjects = gameobjects
        self.computers = computers
        self.day_npcs = day_npcs
        self.night_npcs = night_npcs

    def load(data):
        locations = {}
        for k,v in data.items():
            locations[k] = Location(
                    k,
                    v['desc'],
                    v['connections'],
                    v['gameobjects'],
                    v['computers'],
                    v['day_npcs'],
                    v['night_npcs']
                )
        return locations

    def get_connections(self):
        w = get_world()
        cs = []
        for c in self.connections:
            cs.append(w.get_location(c))
        return cs

    def get_connection(self, con):
        if con in self.connections:
            return get_world().get_location(con)
        return False

    def get_gameobjects(self):
        w = get_world()
        gos = []
        for g in self.gameobjects:
            gos.append(w.get_gameobject(g))
        return gos

    def get_gameobject(self, go):
        if go in self.gameobjects:
            return get_world().get_gameobject(go)
        for g in self.get_gameobjects():
            if g.opened and go in g.specials['contents']:
                return get_world().get_gameobject(go)
        return False

    def remove_gameobject(self, go):
        r = None
        if go in self.gameobjects:
            self.gameobjects.remove(go)
        else:
            r = self.remove_from_container(go)
        return r

    def get_container(self, go):
        g = None
        for n in self.gameobjects:
            g = get_world().get_gameobject(n)
            if 'contents' in g.specials and go in g.specials['contents']:
                return n
        return False

    def remove_from_container(self, go):
        w = get_world()
        name = self.get_container(go)
        cont = w.get_gameobject(name)
        if 'contents' in cont.specials and go in cont.specials['contents']:
            w.gameobjects[name].specials['contents'].remove(go)
            save_world(w)
        return False

    def add_gameobject(self, go):
        if go not in self.gameobjects:
            self.gameobjects.append(go)
            return True
        return False

    def get_npcs(self):
        w = get_world()
        npcs = []
        it = []
        if w.time.now == "day":
            it = self.day_npcs
        elif w.time.now == "night":
            it = self.night_npcs

        for n in it:
            npcs.append(w.get_npc(n))

        return npcs

    def get_npc(self, name):
        if name in self.day_npcs or name in self.night_npcs:
            return get_world().get_npc(name)
        return False

    def get_computers(self):
        w = get_world()
        comps = []
        for c in self.computers:
            comps.append(w.get_computer(c))
        return comps

    def get_computer(self, name):
        if name in self.computers:
            return get_world().get_computer(name)
        return False

    # def move_npc(self, name, loc):
    #     w = get_world()
    #     loc = get_location(loc)
    #     if loc:
    #         self.npcs.remove(name)
    #         loc.npcs.append(name)
    #         w.save_location(loc)
    #         w.save_location(self)
    #         save_world(w)
    #         return True
    #     return False

"""
--------------------------
    GameObject
--------------------------
GameObjects are objects in the world that the player can interact with.
If a GameObject is picked up, then it is considered and "item".
GameObjects affect what actions are avaliable to the player.
"""
class GameObject:
    def __init__(self, name, desc, attrs, specials):
        self.name = name
        self.desc = desc
        self.attrs = attrs
        self.specials = specials
        self.opened = False

    def load(data):
        gameobjects = {}
        for k,v in data.items():
            attributes = []
            specials = {}

            if 'attributes' in data[k]:
                attributes = data[k]['attributes']
            if 'specials' in data[k]:
                specials = data[k]['specials']

            gameobjects[k] = GameObject(
                    k,
                    data[k]['desc'],
                    attributes,
                    specials
                )
        return gameobjects

"""
--------------------------
    Computer
--------------------------
The main object tool the game. You can access a computer like you would access a gameobject. Once you access a computer,
you can types commands into it, and it will return outputs, including text and images.
"""
class Computer(GameObject):
    def __init__(self, name, owner, desc, can_pick_up, data):
        super().__init__(name, desc, [], {})
        if can_pick_up:
            self.attrs.append("can_pick_up")
        self.owner = owner
        self.data = data

    def load(data):
        computers = {}
        for k,v in data.items():
            computers[k] = Computer(
                k,
                data[k]['owner'],
                data[k]['desc'],
                data[k]['can_pick_up'],
                computer_files(k)
            )
        return computers

    def get_owner(self):
        w = get_world()
        if self.owner == player.name:
            return w.player
        else:
            o = w.get_npc(o)
            if o:
                return o
        return False

    def relative_path(self,target,raw):
        if not raw:
            if target:
                return get_world().player.computer_location + [target]
            return get_world().player.computer_location
        return target

    def add_file(self,path,name,contents,raw=False):
        path = self.relative_path(path,raw)
        directory = self.get_directory(path)
        if directory:
            directory[name] = contents
            return True
        return False

    def get_directory(self,path,raw=False):
        path = self.relative_path(path,raw)
        data = self.data
        if len(path) > 0:
            for e in path:
                if e in data:
                    data = data[e]
                else:
                    return False
        return data

    def ls(self,path,raw=False):
        directory = self.get_directory(path)
        for e in directory:
            if isinstance(directory[e],dict):
                e = str(e) + "/"
            print(" ",e)

    # target = w.player.computer_location
    # target.append(inpt[1])
    def cd(self,path,raw=False):
        w = get_world()
        path = self.relative_path(path,raw)

        # can't cd into files
        if len(path[-1].split(".")) > 1:
            return False
        
        data = self.data

        for e in path:
            if e in data:
                data = data[e]
            else:
                if e == "..":
                    if len(path) > 2:
                        self.cd(path[:-2],raw=True)
                        return True
                    elif len(path) == 2:
                        self.cd([],raw=True)
                        return True
                return False

        w.player.computer_location = path
        save_world(w)
        return True

    def open(self,path,raw=False):
        if not "." in path:
            return False
            
        if self.get_directory(path):
            tp = path.split(".")[1]
            if tp == None:
                return False
            elif tp == "png":
                image_manager.open_image(path)
            elif tp == "txt" or tp == "email":
                file_manager.open_text(path)
            else:
                return False
            return True
        return False

    def run(self, path):
        if self.get_directory(path):
            tp = path.split(".")[1]
            if tp == None:
                return False
            else:
                suc = programs.run(self.name, path)
                return suc
        return False

    def prompt_password(self):
        i = input("enter password: ")
        return i == get_password(self.name)

    def add_file(self,path,filename):
        p = self.data
        for i in path:
            p = p[i]
        p[filename] = filename

"""
--------------------------
    Player
--------------------------
Stores all the information about the Player.
Reputation how highly reguarded you are at work.
    - If goes below 0, fired
    - Every 20 increments is a difference in position
        (promotion at 20, 40, 60, 80, etc)
Reputation also affects how other people interact with you.
"""
class Player:
    def __init__(self, name, mode, computer, computer_location, location, inventory, devices, reputation):
        self.name = name
        self.mode = mode
        self.computer = computer
        self.computer_location = computer_location
        self.location = location
        self.inventory = inventory
        self.devices = devices
        self.reputation = reputation
        self.actions = []
        self.talking = None
        self.running = None
        self.using = None
        self.solved_computers = []

    def load(data):
        return Player(
                data['name'],
                data['mode'],
                data['computer'],
                data['computer_location'],
                data['location'],
                data['inventory'],
                data['devices'],
                data['reputation'],
            )

    def init_laptop(self):
        w = get_world()
        
        c = w.get_computer('laptop')
        c.owner = self.name
        w.save_computer(c)

        c = w.get_computer('phone')
        c.owner = self.name
        w.save_computer(c)

        save_world(w)

    def get_computer(self):
        return get_world().get_computer(self.computer)

    def get_current_directory(self):
        if self.computer:
            path = self.computer_location
            directory = False
            return self.get_computer().get_directory(self.computer_location)
        return False

    def get_location(self):
        return get_world().get_location(self.location)

    def get_inventory(self):
        w = get_world()
        inv = []
        for i in self.inventory:
            inv.append(w.get_gameobject(i))
        return inv

    def get_gameobject(self, name):
        if name in self.inventory:
            return get_world().get_gameobject(name)
        return False

    def get_devices(self):
        w = get_world()
        ds = []
        for d in self.devices:
            ds.append(w.get_computer(d))
        return ds

    def get_device(self, name):
        if name in self.devices:
            return get_world().get_computer(name)
        return False

    def enter_computer(self, name):
        w = get_world()
        if name in w.computers:
            self.computer = name
            self.mode = "comp"
            self.computer_location = []
            if not name in self.solved_computers:
                self.solved_computers.append(name)
            return self
        else:
            return False

    def give_item(self, i):
        if isinstance(i, GameObject):
            i = i.name
        elif isinstance(i, list):
            for j in i:
                self.give_item(j)
            return

        if i not in self.inventory:
            self.inventory.append(i)

    def complete_action(self, action):
        if not isinstance(action, str):
            action = action.name

        if action not in self.actions:
            self.actions.append(action)

    def has_items(self, itemlist):
        for i in itemlist:
            if not i in self.inventory:
                return False
        return True

    def has_devices(self, devicelist):
        for i in devicelist:
            if not i in self.devices:
                return False
        return True

"""
--------------------------
    NPC
--------------------------
NPCs are characters in the game that will interact with you in typical ways.
NPCs will take into account your 
However, some NPCs will do special things and be required for certain tasks.
"""
class NPC:
    def __init__(self, name, desc, dialogue):
        self.name = name
        self.desc = desc
        self.location = None
        self.dialogue = dialogue

    def load(data, dialogue_data):
        npcs = {}
        for k,v in data.items():
            npcs[k] = NPC(
                k,
                data[k]['desc'],
                dialogue_data[k]
            )
        return npcs

    def activate_dialogue(self):
        w = get_world()
        dia = ""

        if w.time.now == "night":
            print()
            slow_print("(" + self.name + ") ...zzzzzz...")
            print()
            return True

        if 'reputation' in self.dialogue:
            for r in self.dialogue['reputation']:
                if w.player.reputation >= r[0]:
                    dia = random.choice(r[1])
        
        elif 'time' in self.dialogue:
            for r in self.dialogue['time']:
                if w.time.now == r[0]:
                    dia = random.choice(r[1])
        
        elif 'inventory' in self.dialogue:
            for r in self.dialogue['inventory']:
                if w.player.has_items(r[0]):
                    dia = random.choice(r[1])

        elif 'device' in self.dialogue:
            for r in self.dialogue['device']:
                if w.player.has_devices(r[0]):
                    dia = random.chouce(r[1])
        
        elif 'worldstate' in self.dialogue:
            for r in self.dialogue['worldstate']:
                if w.worldstate == r[0]:
                    dia = random.choice(r[1])
        
        if dia == "":
            dia = random.choice(self.dialogue['default'])

        if "player" in dia:
            dia = dia.replace("player",w.player.name)

        print()
        slow_print("(" + self.name + ") " + str(dia))
        print()

        w.player.talking = self.name
        save_world(w)

        return w

"""
--------------------------
    Time
--------------------------
Time object that stores the current time in the world and has some useful methods
"""
class Time:
    def __init__(self, now):
        self.now = now
        self.possible_times = ["day", "night"]

    def load(data):
        return Time(data['now'])

    def set_time(self, t):
        if t in self.possible_times:
            self.now = t
            return True
        else:
            return False

"""
--------------------------
    Utilities
--------------------------
"""

def fast_print(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()

def slow_print(text,dt=0.0075,br=True):
    for i in list(text):
        time.sleep(dt)
        fast_print(i)
    time.sleep(dt)
    if br:
        lb()

def lb():
    sys.stdout.write("\n")
    sys.stdout.flush()