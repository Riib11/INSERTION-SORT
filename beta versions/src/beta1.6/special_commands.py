# some commands don't work on windows...

import sys
from subprocess import call

rows = 25
cols = 100
screensize = "\x1b[8;{rows};{cols}t".format(rows=rows, cols=cols)

def format_screen():
    sys.stdout.write(screensize)

def clear():
    format_screen()
    # try:
    #     call(['clear'], shell=True)
    # except:
    #     try:
    #         call(['cls'], shell=True)
    #     except:
    for i in range(rows):
        print()

clear()