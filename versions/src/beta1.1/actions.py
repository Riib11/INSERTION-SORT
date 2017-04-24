from accessor import *
import sys
import time

class ActionManager:
    def __init__(self, actions):
        self.actions = actions

    def load(data):
        actions = {}
        for k,v in data.items():
            actions[k] = Action(
                k,
                v['single'],
                v['requirements'],
                v['results']
            )
        return ActionManager(actions)

    def avaliable(self):
        w = get_world()
        ava = []
        for k,v in self.actions.items():
            if v.is_avaliable(w=w):
                ava.append(v)
        return ava

    def run_avaliable(self):
        ava = self.avaliable()
        w = get_world()
        for a in ava:
            w = a.run(w=w)
        return w


"""
--------------------------
    Action
--------------------------
Player does actions, and this is how the player progresses through the game.
In order to do an action, the player must fulfill the requirements for the action (location, reputation, gameobjects.
If the player successfully does the action, they get the results of the action, which can include:
    - reputation
    - aquiring GameObjects
    - changing Location
    - changing Location of an NPC
    - other things?
"""
class Action:
    def __init__(self, name, single, requirements, results):
        self.name = name
        self.single = bool(single)
        self.done = False
        self.requirements = requirements
        self.results = results

    def run(self, w=None):
        if w == None:
            w = get_world()

        self.done = True
        w.player.complete_action(self)

        quiet = False

        res = self.results

        if 'dialogue' in res:
            print()
            slow_print("{!} " + res['dialogue'])
            print()
        else:
            quiet = True

        w.action_manager.actions[self.name] = self

        if 'reputation' in res:
            w.player.reputation += res['reputation']
            if res['reputation'] > 0:
                s = "gained"
            elif res['reputation'] < 0:
                s = "lost"
            rep = str(abs(res['reputation']))
            if not quiet:
                slow_print("{*} you " + s + " " + rep + " reputation.")
        
        if 'location' in res:
            w.player.mode = "real"
            w.player.location = res['location']
            if not quiet:
                slow_print("{@} you are now at: " + res['location'] + ".")
        elif 'mode' in res:
            w.player.mode = res['mode']
        
        if 'items' in res:
            w.player.give_item(res['items'])
            s = "{$} you got: "
            for i in res['items']:
                s += i + ", "
            s = s[:-2] + "."
            if not quiet:
                slow_print(s)
        
        if 'devices' in res:
            w.player.give_device(res['devices'])
            s = "{$} you got: "
            for i in res['devices']:
                s += i + ", "
            s = s[:-2] + "."
            if not quiet:
                slow_print(s)
        
        if 'time' in res:
            w.time.now = res['time']
            if not quiet:
                slow_print("{∆} it is now " + res['time'] + ".")
        
        if 'computer_file' in res:
            res = res['computer_file']
            c = w.get_computer(res[0])
            raw = res[1]
            path = raw.split("/")[:-1]
            filename = raw.split("/")[-1]
            c.add_file(path,filename)
            w.save_computer(c)
            if res[2] == "public":
                if not quiet:
                    slow_print("{>} a file has been added on " + c.name)
            elif res[2] == "hint":
                if not quiet:
                    slow_print("{>} a file has been changed somewhere...")
            if res[2] == "secret":
                pass

        if 'computer_files' in res:
            res = res['computer_files']
            for comp_file in res:
                c = w.get_computer(comp_file[0])
                raw = comp_file[1]
                path = raw.split("/")[:-1]
                filename = raw.split("/")[-1]
                c.add_file(path,filename)
                w.save_computer(c)
                if comp_file[2] == "public":
                    if not quiet:
                        slow_print("{>} a file has been added on " + c.name)
                elif comp_file[2] == "hint":
                    if not quiet:
                        slow_print("{>} a file has been changed somewhere...")
                if comp_file[2] == "secret":
                    pass

        if 'take' in res:
            for i in res['take']:
                w.player.inventory.remove(i)
                slow_print("{-$} " + i + " was taken from you.")

        if 'eat' in res:
            for i in res['eat']:
                w.player.inventory.remove(i)
                slow_print("you ate the " + str(i) + ".")

        if 'gamestate' in res:
            w.worldstate = res['gamestate']

        if 'place object' in res:
            go = res['place object'][0]
            locname = res['place object'][1]
            loc = w.get_location(locname)
            s = loc.add_gameobject(go)
            if s:
                slow_print("{!} " + go + " was put in " + locname + ".")
                w.save_location(loc)

        if not quiet:
            print()

        return w

    def is_avaliable(self, w=None):
        if w == None:
            w = get_world()

        if self.single and self.done:
            return False

        reqs = self.requirements

        if 'talking' in reqs:
            if not any(x == w.player.talking for x in reqs['talking']):
                return False
        
        if 'reputation' in reqs:
            if not w.player.reputation >= reqs['reputation']:
                return False

        if 'under reputation' in reqs:
            if not w.player.reputation <= reqs['under reputation']:
                return False

        if 'using' in reqs:
            if not any(x == w.player.using for x in reqs['using']):
                return False
        
        if 'locations' in reqs:
            if not w.player.location in reqs['locations']:
                return False
        
        if 'items' in reqs:
            if not all(x in w.player.inventory for x in reqs['items']):
                return False
        
        if 'devices' in reqs:
            if not all(x in w.player.devices for x in reqs['devices']):
                return False
        
        if 'computer' in reqs:
            if not any(x == w.player.computer for x in reqs['computer']):
                return False
        
        if 'mode' in reqs:
            if w.player.mode != reqs['mode']:
                return False
        
        if 'time' in reqs:
            if w.time.now != reqs['time']:
                return False

        if 'solved' in reqs:
            if not all(x in w.player.solved_computers for x in reqs['solved']):
                return False

        return True


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