import console
import world
import scenes
import display
import time
import sys
from subprocess import call
from accessor import *
from debug import *

class Game:
    def __init__(self,load_name, new):

        self.new = new

        # update the accessor to reference this game as the current game
        set_current_game(load_name)

        # try adding this game to SavesManager's saves
        try:
            add_save(load_name, world.World())
        
        # if doesn't work, that means that it needed to run once in order to get SavesManager running again, so have to quit and start over
        except TypeError:
            call(["clear"])
            print("[!!] you just reset saves, so the system needed to reboot. restart the game to play.")
            print("+=====================================================================================+")
            sys.exit()

        call(["clear"])

        bar     = "+----------------------------------------------------+"
        newgame = bar  + "\n| - NEW -                                            |\n" + bar
        loadgame = bar + "\n| - LOADING -                                        |\n" + bar

        # get the name of player if a new game
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

    # main function to start the game
    # facilitates update loop
    def run(self):
        w = get_world()

        # the game needs to be set to running again
        if w.running == False:
            # the game is being continued
            w.running = True
            save_world(w)
        
        # show the intro to the game
        if self.new:
            scenes.intro()
        else:
            call(['clear'])

        # run game tilled stopped
        w = get_world()
        while w.running == True:
            # update the world
            w = self.update()
            self.console.prompt()
            # update local world object after input in order to check for w.running
            w = get_world()

    def update(self):
        w = get_world()
        # run actions that have their requirements met
        w = w.action_manager.run_avaliable()
        # update the world
        w.update()
        # save the updated world to the save file
        save_world(w)
        # return for Game's reference
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