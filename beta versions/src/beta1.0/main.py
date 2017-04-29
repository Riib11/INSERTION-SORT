from subprocess import call
import game
from game import Game
import time
import sys
from accessor import *

def buffered_input(prompt,acceptable={}, gen_acceptable=[], unacceptable=[]):
    i = input(prompt).lower()

    if i == "quit":
        sys.exit()

    if i == "":
        print("an empty string is not valid")
        print()
        return buffered_input(prompt, acceptable=acceptable, gen_acceptable=gen_acceptable, unacceptable=unacceptable)

    if len(acceptable) != 0:
        while i not in acceptable:
            print("[!] sorry, that didn't make sense.")
            print()
            i = input(prompt).lower()
            if i == "quit":
                sys.exit()
        print()
        return acceptable[i]
    elif len(gen_acceptable) != 0:
        while i not in gen_acceptable:
            print("[!] sorry, that isn't avalaible.")
            print()
            i = input(prompt).lower()
            if i == "quit":
                sys.exit()
        print()
        return i
    elif len(unacceptable) != 0:
        while i in unacceptable:
            if i == "quit":
                sys.exit()
            print("[!] sorry, you can't use that.")
            print()
            i = input(prompt).lower()
        print()
        return i

def fast_print(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()

def slow_print(text,dt=0.005,br=True):
    for i in list(text):
        time.sleep(dt)
        fast_print(i)
    time.sleep(dt)
    if br:
        lb()

def lb():
    sys.stdout.write("\n")
    sys.stdout.flush()

call(["clear"])

bar     = "+----------------------------------------------------+"
loading = bar + "\n| - INSERTIONSORT -                                  |\n" + bar
newgame = bar + "\n| - NEW -                                            |\n" + bar
loadgame= bar + "\n| - LOAD -                                           |\n" + bar


slow_print(loading);
print()

if len(get_saves()) == 1:
    slow_print("no save files detected...", dt=0.05, br=False)
    time.sleep(0.75)
    new = True
else:
    try:
        new = buffered_input("start new game? ", acceptable={
                "y": True,
                "yes": True,
                "n": False,
                "no": False
            })

    except KeyboardInterrupt:
        call(["clear"])
        print(loading)
        print()
        delete = buffered_input("are you sure you want to delete all save files? ", acceptable={
                "y": True,
                "yes": True,
                "n": False,
                "no": False
            })
        if delete:
            print()
            print("ok, deleting all saves...")

            reset_saves()

            print()
            print("please restart the game. this program will now close.")
            print("+=====================================================================================+")
            sys.exit()
        else:
            print("ok, won't delete files then. please restart that game. this program will now close.")
            print("+=====================================================================================+")
            sys.exit()

load_name = None

call(['clear'])

try:
    if new:
        print(newgame)
        print()
        load_name = buffered_input("name of new game? ", unacceptable=get_saves())
    else:
        print(loadgame)
        print()
        slow_print("--------------------")
        slow_print("avaliable saves:")
        slow_print("--------------------")
        print()
        for s in get_saves():
            if s!=None:
                slow_print("  #=" + len(s)*"=" + "=#")
                slow_print("• | " + s + " |")
                slow_print("  #=" + len(s)*"=" + "=#")
                print()
        slow_print("--------------------")
        load_name = buffered_input("name of save? ", gen_acceptable=get_saves())
except KeyboardInterrupt:
    call(["clear"])
    print(loading)
    print()
    delete = buffered_input("are you sure you want to delete all save files? ", acceptable={
            "y": True,
            "yes": True,
            "n": False,
            "no": False
        })
    if delete:
        print()
        print("ok, deleting all saves...")

        reset_saves()

        print()
        print("please restart the game. this program will now close.")
        sys.exit()

G = Game(load_name, new)

G.run()
print("+=====================================================================================+")

