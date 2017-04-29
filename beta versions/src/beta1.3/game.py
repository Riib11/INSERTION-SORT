import console
import world
import scenes
import display
import time
import sys
from subprocess import call
from accessor import *
from debug import *

def test_add_save(name):
    add_save(name, world.World())

class Game:
    def __init__(self,load_name, new):

        self.new = new

        set_current_game(load_name)

        try:
            add_save(load_name, world.World())
        except TypeError:
            call(["clear"])
            print("[!!] you just reset saves, so the system needed to reboot. restart the game to play.")
            print("+=====================================================================================+")
            sys.exit()

        call(["clear"])

        bar     = "+----------------------------------------------------+"
        newgame = bar  + "\n| - NEW -                                            |\n" + bar
        loadgame = bar + "\n| - LOADING -                                        |\n" + bar

        if new:
            print(newgame)
            print()
            w = get_world()
            w.player.name = input("your name: ")

            while w.player.name == "":
                print("that is a bad name, try again.")
                print()
                w.player.name = input("your name: ")                

            save_world(w)
            w.player.init_laptop()

        else:
            print(loadgame)
            print()
            fast_print("loading")
            slow_print("....................................",dt=.02)
            print()
            input("press enter to continue.")


        # setup console
        self.console = console.Console()

    def run(self):
        w = get_world()
        if w.running == False:
            # the game is being continued
            w.running = True
            save_world(w)
        
        if self.new:
            # show the intro to the game
            scenes.intro()
        else:
            call(['clear'])

        # run game tilled stopped
        w = get_world()
        while w.running == True:
            w = self.update()
            self.console.prompt()
            w = get_world()

    def update(self):
        w = get_world()
        w = w.action_manager.run_avaliable()
        w.update()
        save_world(w)
        return w


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