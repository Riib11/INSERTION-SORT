from subprocess import call
import game
from game import Game
import time
import sys
from accessor import *

# this allows you to get input that is filtered by either
# - acceptable inputs
# - unnacceptable input
# (gen_acceptable just changes the error message to be 'sorry, that isn't avaliable')
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
# for printing things that may be inside loops
def fast_print(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()

# a type-writer effect kind of print.
# - dt: how long to delay between each character printed
# - br: put a line break at end of print
def slow_print(text,dt=0.005,br=True):
    for i in list(text):
        time.sleep(dt)
        fast_print(i)
    time.sleep(dt)
    if br:
        lb()
# fast-printed line break
def lb():
    sys.stdout.write("\n")
    sys.stdout.flush()

call(["clear"])

bar     = "+----------------------------------------------------+"
loading = bar + "\n| - INSERTIONSORT -                                  |\n" + bar
newgame = bar + "\n| - NEW -                                            |\n" + bar
loadgame= bar + "\n| - LOAD -                                           |\n" + bar

# the main bar at top of screen
slow_print(loading);
print()

# if there are no save files avaliable, then they cannot get the option to continue a saved game
if len(get_saves()) == 1:
    slow_print("no save files detected...", dt=0.05, br=False)
    time.sleep(0.75)
    new = True

# give player option to start a new game or to continue a saved game
else:
    try:
        new = buffered_input("start new game? ", acceptable={
                "y": True,
                "yes": True,
                "n": False,
                "no": False
            })

    # allow use to CTRL-c to go to special menu for deleting all save files
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
    # if they decided to make a new game
    if new:
        print(newgame)
        print()
        load_name = buffered_input("name of new game? ", unacceptable=get_saves())

    # they decided to continue a saved game
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

# allow use to CTRL-c to go to special menu for deleting all save files
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

# create new game object to facilitate the game
G = Game(load_name, new)

# run game, which will loop until done
G.run()

print("+=====================================================================================+")

