from accessor import *
import code
from debug import *
from subprocess import call
import time
import sys
import programs

"""
--------------------------
    Commands
--------------------------
Commands abstract class
"""
class Commands:
    def __init__(self):
        self.commands_map = {}

    def run(self,s,inpt):
        self.commands_map[s](inpt)

    def is_command(self,s):
        if s in self.commands_map:
            return True
        return False

    def get_commands_from(self,s):
        for c in s:
            if self.is_command(c):
                return self.commands_map[c]
        return None

"""
--------------------------
    World Commands
--------------------------
Commands that are done in the real world.
"""
class WorldCommands(Commands):
    def __init__(self):
        super().__init__()
        self.commands_map = {
            # if error on input
            "__nocmd": self.nocmd,
            "__bad": self.bad,
            # other commands
            "help": self.h,
            "h": self.h,
            "help!": self.help1,
            "?": self.h,
            "info": self.info,
            "solved": self.solved,
            "go": self.go,
            "gt": self.go,
            "clear": self.clear,
            "inventory": self.inventory,
            "i": self.inventory,
            "take": self.take,
            "t": self.take,
            "drop": self.drop,
            "d": self.drop,
            "open": self.open,
            "o": self.open,
            "close": self.close,
            "talk": self.talk,
            "tt": self.talk,
            "use": self.use,
            "u": self.use,
            "nearby": self.nearby,
            "n": self.nearby,
            "explore": self.explore,
            "e": self.explore,
            "inspect": self.inspect,
            "in": self.inspect,
            "read": self.inspect,
            "r": self.inspect,
            "quit": self.quit,
            "q": self.quit,
            "wow": self.wow
        }

    def get_avaliable(self):
        return [
            ["help","get basic informtion and avaliable commands. (h)"],
            ["help!","get more detailed help"],
            ["info", "check your watch and think about important information and such."],
            ["solved", "check what passwords you've figured out."],
            ["go to ___","travel to a desired (nearby) location. (gt)"],
            ["talk to ___","be social. (tt)"],
            ["inventory","your stuff. (i)"],
            ["take ___","take something. (t)"],
            ["drop ___","drop something. (d)"],
            ["open ___","open something that's holding stuff. (o)"],
            ["use ___","use a computer or a thing (in you inventory or nearby). (u)"],
            ["inspect / read ___","take a closer look at an object. (in / r)"],
            ["nearby", "get a list of nearby locations. (n)"],
            ["explore", "look around. (e)"],
        ]

    def h(self, inpt):
        w = get_world()
        print()
        print("help:")
        print("  you are:", w.player.name)
        print("  your location:", w.player.location)
        print("  your reputation:", w.player.reputation)
        print("  the time is:", w.time.now)
        print("  symbols: - (item), > (device), * (character), ~ (place)")
        print("  you can:   ")
        for c in self.get_avaliable():
            print("    -",c[0],":",c[1])
        print()

    def help1(self, inpt):
        print()
        print("detailed help:")
        print("--------------")
        print("# symbols: - (item), > (device), * (character), ~ (place)")
        print("# nearby locations: 'nearby' this lists the locations that are near enough to you that you can use the 'go to' command to go to them.")
        print("these symbols are next to the things that pop up when you 'explore'.")
        print("# inventory: these are the items that you have on you, and stay with you as you go from place to place. you can inspect and use items in your inventory just like an item in the environment.")
        print("# taking and dropping: you can take some items in your environment. they get stored in your inventory when you take them, and when you drop them they just go into the current room.")
        print("# opening: some items can be opened. if you open something, you can look at its contents by using 'explore'")
        print("# using: 'using' is the general term for interacting with something (only some things can be used). for example, you can use your phone, bed, and laptop.")
        print("# inspecting: you can inspect anything. this is basically just the action of looking at something or someone and noticing things about them/it.")
        print()

    def info(self, inpt):
        w = get_world()
        print()
        print("  you are:", w.player.name)
        print("  your location:", w.player.location)
        print("  your reputation:", w.player.reputation)
        print("  the time is:", w.time.now)
        print()

    def solved(self, inpt):
        w = get_world()
        print()
        print("  passwords you've cracked:")
        for c in w.player.solved_computers:
            print("    <" + c + "> " + str(get_password(c)))
        print()

    def wow(self, inpt):
        print()
        print("wow indeed.")
        print()

    def inventory(self, inpt):
        w = get_world()
        print()
        print("you have")
        for i in get_world().player.devices:
            print("  >",i)
        for i in get_world().player.inventory:
            print("  -",i)
            if w.get_gameobject(i).opened:
                for j in w.get_gameobject(i).specials['contents']:
                    print("     -",j.name)
        print()

    def take(self, inpt):
        if len(inpt) < 2:
            self.bad(inpt)
            return False
        w = get_world()
        target = inpt[1]
        go = w.player.get_location().get_gameobject(target)
        c = w.player.get_location().get_computer(target)
        if go:
            if 'can_pick_up' in go.attrs:
                if len(w.player.inventory) < 7:
                    loc = w.player.get_location()
                    loc.remove_gameobject(target)
                    w = get_world()
                    w.save_location(loc)
                    w.player.give_item(target)
                    print()
                    print("(you take the",target + ".)")
                    print()
                    save_world(w)
                else:
                    print()
                    print("(you'd like to take that, but you've got too much stuff in your inventory.)")
                    print()
            else:
                print()
                print("(you can't take that)")
                print()
        elif c:
            if 'can_pick_up' in c.attrs:
                loc = w.player.get_location()
                loc.computers.remove(target)
                w.save_location(loc)
                w.player.devices.append(target)
                print()
                print("(you take the",target + ".)")
                print()
                save_world(w)
            else:
                print()
                print("(you can't take that)")
                print()
        else:
            self.bad(inpt)

    # sometimes can't drop things?
    def drop(self, inpt):
        if len(inpt) < 2:
            self.bad(inpt)
            return False
        w = get_world()
        target = inpt[1]
        if target in w.player.inventory:
            w.player.inventory.remove(target)
            loc = w.player.get_location()
            loc.gameobjects.append(target)
            w.save_location(loc)
            print()
            print("(you drop the",target + ".)")
            print()
            save_world(w)
        elif target in w.player.devices:
            w.player.devices.remove(target)
            loc = w.player.get_location()
            loc.computers.append(target)
            w.save_location(loc)
            print()
            print("(you drop the",target + ".)")
            print()
            save_world(w)
        else:
            self.bad(inpt)

    def open(self, inpt):
        if len(inpt) < 2:
            self.bad(inpt)
            return False
        w = get_world()
        t = inpt[1]
        loc = w.player.get_location()
        go = loc.get_gameobject(t)
        it = w.player.get_gameobject(t)
        if go:
            if 'contents' in go.specials:
                if go.opened:
                    print()
                    print("(its already open)")
                    print()
                else:
                    go.opened = True
                    print()
                    print("(you opened the " + t + ")")
                    print()
                    w.save_gameobject(go)
            else:
                print()
                print("(you can't open that)")
                print()
        elif it:
            if 'contents' in it.specials:
                if it.opened:
                    print()
                    print("(its already open)")
                    print()
                else:
                    it.opened = True
                    print()
                    print("(you opened the " + t + ")")
                    print()
                    w.save_gameobject(it)
            else:
                print()
                print("(you can't open that)")
                print()
        else:
            self.bad(inpt)
        save_world(w)

    def close(self, inpt):
        if len(inpt) < 2:
            self.bad(inpt)
            return False

    def go(self, inpt):
        target = "none"
        if len(inpt) == 2:
            target = inpt[1]
        elif len(inpt) == 3:
            target = inpt[2]
        else:
            self.bad(inpt)
            return False

        if target == "sleep":
            self.use(["use","bed"])
            return True
        
        w = get_world()
        loc = w.player.get_location().get_connection(target)
        if loc:
            w.player.location = target
            print()
            print("(you go to ",target + ". " + loc.desc + ")")
            print()
            save_world(w)
        else:
            self.bad(inpt)

    def talk(self, inpt):
        if len(inpt) == 3:
            target = inpt[2]
        elif len(inpt) == 2:
            target = inpt[1]
        else:
            self.bad(inpt)
            return False

        w = get_world()
        target = w.get_npc(target)
        if target:
            target.activate_dialogue()
        else:
            self.bad(inpt)

    def use(self, inpt):
        if len(inpt) < 2:
            self.bad(inpt)
            return False

        t = inpt[1]
        w = get_world()

        if t == "bed":
            if w.player.get_location().name == "bedroom":
                print()

                if not 'first-day' in w.player.actions:
                    print("[!] you can't sleep now! you need to go to work, its your first day.")
                    print()
                    return False

                wake = input("when do you want to wake up? ")
                suc = w.time.set_time(wake)
                if suc:
                    w.player.using = "bed"
                    save_world(w)
                    slow_print("you fall",dt=0.05)
                    slow_print(" asleep...",dt=0.2);lb()
                    print()
                    print("(it is now " + wake + ")")
                else:
                    validtimes = w.time.possible_times
                    vtstr = ""
                    for t in validtimes:
                        vtstr += "'" + str(t) + "', "
                    vtstr = vtstr[:-2]
                    print("(that's not a valid time. valid times are: " + vtstr + ".)")
                print()
            else:
                print()
                print("(you can only sleep in your bedroom!)")
                print()
        elif t == "car":
            if "car" in w.player.get_location().connections:
                self.go(["go to", "car"])
                w.player.using = "car"
                return True
            print()
            print("(your car isn't near here)")
            print()
        else:
            go = w.player.get_location().get_gameobject(t)
            item = w.player.get_gameobject(t)
            c = w.player.get_location().get_computer(t)
            comp = w.player.get_device(t)
            if go:
                if 'active' in go.specials:
                    print()
                    print("(" + go.specials['active'] + ")")
                    print()
                    w.player.using = t
                elif 'eat' in go.specials:
                    print()
                    print("(" + go.specials['eat'] + ")")
                    print()
                    w.player.inventory.remove(t)
                    w.player.using = t
                    save_world(w)
                else:
                    print()
                    print("(you can't use that)")
                    print()
            elif item:
                if 'active' in item.specials:
                    print()
                    print("(" + item.specials['active'] + ")")
                    print()
                    w.player.using = t
                elif 'eat' in item.specials:
                    print()
                    print("(" + item.specials['eat'] + ")")
                    print()
                    w.player.inventory.remove(t)
                    w.player.using = t
                    save_world(w)
                else:
                    print()
                    print("(you can't use that)")
                    print()
            elif comp or c:
                can_use = True

                # can't use someone else's computer during the day!
                if comp and comp.owner != w.player.name and w.time.now == "day":
                    can_use = False
                elif c and c.owner != w.player.name and w.time.now == "day":
                    can_use = False

                if can_use:
                    print()
                    fast_print("entering " + t)
                    slow_print("...");lb();
                    suc = False
                    if comp:
                        suc = comp.prompt_password()
                    else:
                        suc = c.prompt_password()

                    if suc:
                        print("[success]")
                        # also adds to solved computers if not already solved
                        player = w.player.enter_computer(t)
                        w.player = player
                        save_world(w)
                    else:
                        print("[failure]")
                        print()
                else:
                    print()
                    print("(you can't use someone else's computer right in front of them!)")
                    print()
            else:
                self.bad(inpt)

    def nearby(self, inpt):
        w = get_world()
        print()
        print("near here are:")
        for loc in w.player.get_location().connections:
            print("  ~",loc)
        print()

    def explore(self, inpt):
        w = get_world()
        print()

        if len(w.player.get_location().get_npcs()) == 0 and len(w.player.get_location().get_computers()) == 0 and len(w.player.get_location().get_gameobjects()) == 0:
            print("there's nothing here.")
        
        else:
            print("in this area there are:")
            for npc in w.player.get_location().get_npcs():
                print("  *",npc.name)
            for comp in w.player.get_location().get_computers():
                print("  >",comp.name)
            for go in w.player.get_location().get_gameobjects():
                print("  -",go.name)
                if go.opened:
                    for i in go.specials['contents']:
                        print("     -",i)
        print()

    def inspect(self, inpt):
        if len(inpt) < 2:
            self.bad(inpt)
            return False
        w = get_world()
        loc = w.player.get_location()
        desc = ""
        if inpt[1] in loc.gameobjects:
            desc = loc.get_gameobject(inpt[1]).desc
        elif inpt[1] in loc.day_npcs or inpt[1] in loc.night_npcs:
            desc = loc.get_npc(inpt[1]).desc
        elif inpt[1] in loc.computers:
            desc = loc.get_computer(inpt[1]).desc
        elif inpt[1] in w.player.devices:
            desc = w.player.get_device(inpt[1]).desc
        elif inpt[1] in w.player.inventory:
            desc = w.player.get_gameobject(inpt[1]).desc
        else:
            for go in w.player.get_location().get_gameobjects():
                if go.opened:
                    if inpt[1] in go.specials['contents']:
                        desc = w.get_gameobject(inpt[1]).desc
                        break
            if desc == "":
                self.bad(inpt)
                return False

        print()
        print("(" + desc + ")")
        print()

    def clear(self, inpt):
        call(['clear'])

    def quit(self, inpt):
        print("------------------------------------------------------")
        print("[!] your progress is saved")
        i = input("Are you sure you want to quit? ")
        if i != None:
            if i[0] == "y":
                print("Quitting game...")
                w = get_world()
                w.running = False
                save_world(w)
                return True
        print("ok, game is continuing")
        print("------------------------------------------------------")
        print()
        return False

    def nocmd(self, inpt):
        out = ""
        if len(inpt) >= 1:
            print()
            print("(sorry, couldn't do '" + inpt[0] + "')")
            print()
        else:
            print()
            print("(no command found)")
            print()

    def bad(self, inpt):
        print()
        print("(couldn't " + inpt[0] + " like that.)")
        print()

"""
--------------------------
    Computer Commands
--------------------------
Commands that are done on a computer.
"""
class ComputerCommands(Commands):
    def __init__(self):
        super().__init__()
        self.commands_map = {
            # if error on input
            "__nocmd": self.nocmd,
            "__bad": self.bad,
            # other commands
            "help": self.h,
            "help!": self.help1,
            "info": self.info,
            "ls": self.ls,
            "cd": self.cd,
            "clear": self.clear,
            "open": self.open,
            "run": self.run_program,
            "exit": self.exit,
            "quit": self.quit,
            "q": self.quit
        }

    def get_avaliable(self):
        return [
            ["help","get basic informtion and avaliable commands"],
            ["info","get basic information"],
            ["ls", "list the contents of the current directory"],
            ["cd [dir]","enter a directory ('cd ..' goes up a directory)"],
            ["open [file]","open a file"],
            ["run [executable]", "run a program"],
            ["exit","exit the terminal"],
        ]

    def h(self, inpt):
        w = get_world()
        print("computer help menu:")
        print("    computer name:       ", w.player.computer)
        loc = [w.player.computer] + w.player.computer_location
        print("    current directory:   ", code.arr_to_path(loc))
        print("    current time:        ", w.time.now)
        print("    avaliable commands:  ")
        for c in self.get_avaliable():
            print("      -",c[0],":",c[1])

    def help1(self, inpt):
        print("  ls: use this to list everything in the current directory.")
        print("  cd [dir]: go to a directory that is inside the current one. if you want to go up a directory, use 'cd ..'")
        print("  open [file]: you can only open .txt .email and .png files")
        print("  run [executable]: if the file ending is something wierd like .sh or .exe. or .x then you can probably run it.")

    def info(self, inpt):
        w = get_world()
        print("computer help menu:")
        print("    computer name:       ", w.player.computer)
        loc = [w.player.computer] + w.player.computer_location
        print("    current directory:   ", code.arr_to_path(loc))
        print("    current time:        ", w.time.now)

    def ls(self, inpt):
        get_world().player.get_computer().ls(False)

    def cd(self, inpt):
        if len(inpt) < 2:
            self.bad(inpt)
            return False
        suc = get_world().player.get_computer().cd(inpt[1])
        if not suc:
            self.bad(inpt)

    def open(self, inpt):
        if len(inpt) < 2:
            self.bad(inpt)
            return False
        suc = get_world().player.get_computer().open(inpt[1])
        if not suc:
            self.bad(inpt)

    def run_program(self, inpt):
        if len(inpt) < 2:
            self.bad(inpt)
            return False
        c = get_world().player.get_computer()
        suc = c.run(inpt[1])
        if not suc:
            self.bad(inpt)

    def clear(self, inpt):
        call(['clear'])

    def exit(self, inpt):
        w = get_world()
        w.player.mode = "real"
        save_world(w)
        fast_print("exiting " + w.player.computer)
        slow_print("...")
        lb()
        print()
        print("(you exit out of the " + w.player.computer + ".)")
        print()

    def quit(self, inpt):
        print("------------------------------------------------------")
        print("[!] your progress is saved")
        i = input("Are you sure you want to quit? ")
        if i != None:
            if i[0] == "y":
                print("Quitting game...")
                w = get_world()
                w.running = False
                save_world(w)
                return True
        print("ok, game is continuing")
        print("------------------------------------------------------")
        print()
        return False

    def nocmd(self, inpt):
        if len(inpt) >= 1:
            print("-terminal:",inpt[0],": command not found")

    def bad(self, inpt):
        print("-terminal: incorrect use of",inpt[0])

def fast_print(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()

def slow_print(text,dt=0.2):
    for i in list(text):
        time.sleep(dt)
        fast_print(i)
    time.sleep(dt)
    
def lb():
    sys.stdout.write("\n")
    sys.stdout.flush()