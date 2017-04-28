# some commands don't work on windows...

import sys
from subprocess import call

def clear():
    for i in range(25):
        print()
    # try:
    #     call(['clear'], shell=True)
    # except:
    #     try:
    #         call(['cls'], shell=True)
    #     except:
