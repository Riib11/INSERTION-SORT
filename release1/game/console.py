from debug import *
from accessor import *
import code
import time
from subprocess import call
import sys
from commands import WorldCommands
from commands import ComputerCommands

"""
--------------------------
    Console
--------------------------
The main interface for hte player. Displays output to the player as well as recieves direct input.
"""
class Console:
    def __init__(self):
        self.input_manager = InputManager()

    def prompt(self):
        w = get_world()
        mode = w.player.mode
        if mode == "real":
            inpt = input("# " + w.player.name + " # ")
            self.input_manager.real_interpret(inpt.split())
        elif mode == "comp":
            inpt = input("" + code.comp_input_header() + "")
            self.input_manager.comp_interpret(inpt.split())

"""
--------------------------
    Input Manager
--------------------------
Is the prime manager of all input. Filters input to computer and world commands.
"""
class InputManager:
    def __init__(self):
        self.world_commands = WorldCommands()
        self.computer_commands = ComputerCommands()

    def comp_interpret(self, inpt):
        cmd = None
        
        for s in inpt:
            if self.computer_commands.is_command(s):
                cmd = s
                break

        if cmd != None:
            self.computer_commands.run(s,inpt)
        else:
            self.computer_commands.run("__nocmd", inpt)

    def real_interpret(self, inpt):
        cmd = None
        
        for s in inpt:
            if self.world_commands.is_command(s):
                cmd = s
                break

        if cmd != None:
            self.world_commands.run(s,inpt)
        else:
            self.world_commands.run("__nocmd", inpt)