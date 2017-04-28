import time
from special_commands import clear
import special_commands
import sys
import random
from accessor import *
random.seed()

rows = 25
cols = 100
screensize = "\x1b[8;{rows};{cols}t".format(rows=rows, cols=cols)

def format_screen():
    sys.stdout.write(screensize)

def intro():
    try:
        sys.stdout.write(screensize)
        clear()

        # title

        length = 300
        title_time = 100
        dt = 0.025

        bar = "/-----/-----/-----/-----/-----/-----/-----/-----/-----/-----/-----/-----/-----/-----/-----/-----/--"
        bar = bar[0:cols]

        titles = [
            "           > INSERTIONSORT <",
            "                   a game by",
            "                       henry blanchette"
        ]

        glitch_titles = [
            "                 NSGT SOFF  ??? ' '' #                        T SOFF  ???",
            "        --   595  95 --              00  010111011111 111110 0 0",
            "                 dd    ** --aajajjajjajja -- --  ||||| code=32498 |||||"
        ]

        for i in range(len(bar)):
            clear()
            fast_print(bar[:i]);lb()
            fast_print(cycle(bar)[:i]);lb()
            fast_print(cycle(cycle(bar))[:i]);lb()
            lb()
            for t in titles:
                lb()
            lb()
            fast_print(bar[:i]);lb()
            fast_print(cycle(bar)[:i]);lb()
            fast_print(cycle(cycle(bar))[:i])
            time.sleep(dt)

        
        counter = 0
        for i in range(length):
            clear()
            fast_print(bar);lb()
            fast_print(cycle(bar));lb()
            fast_print(cycle(cycle(bar)));lb()
            lb()
            if i > title_time:
                counter += 1

                if counter > 20:
                    for i in range(len(titles)):
                        titles[i] = " " + titles[i]
                    counter = 0

                for t in titles:
                        fast_print(t);lb()
            else:
                lb()
                lb()
                lb()

            lb()
            fast_print(bar);lb()
            fast_print(cycle(bar));lb()
            fast_print(cycle(cycle(bar)))

            bar = cycle(bar)
            time.sleep(dt)

        clear()
        
        # glitching
        
        counter = 0
        dt = 0.125
        glitch = False

        for i in range(length//10):
            clear()
            fast_print(bar);lb()
            fast_print(cycle(bar));lb()
            fast_print(cycle(cycle(bar)));lb()
            lb()
            if glitch:
                for t in glitch_titles:
                    fast_print(t);lb()
            else:
                for t in titles:
                    fast_print(t);lb()
            
            counter += 1
            if counter > 3:
                glitch = not glitch
                counter -= random.randint(2,4)
                time.sleep(dt)
            
            lb()
            fast_print(bar);lb()
            fast_print(cycle(bar));lb()
            fast_print(cycle(cycle(bar)))

            bar = cycle(cycle(cycle(cycle(bar))))
            time.sleep(dt)

        clear()

        time.sleep(2.5)

        # loading    

        min_cycles = 20
        max_cycles = 50
        max_wait = .001
        min_wait = .05

        titles = ["writing code", "generating locations", "creating gameobjects", "designing characters", "creating personalities", "fashioning nuances", "defining 'justice'", "feeding cats", "drawing images", "creating <?>evil_scheme<?>", "���%����%����", "writing plot", "writing more code", ":3", "reviewing plot", "approving plot", "solving equations"]

        for t in titles:
            fast_print(t)
            for i in range(random.randint(min_cycles,max_cycles)):
                fast_print(".")
                time.sleep(random.uniform(max_wait,min_wait))
            lb()

        fast_print("debugging")
        for i in range(random.randint(min_cycles*8,max_cycles*8)):
            fast_print(".")
            time.sleep(random.uniform(max_wait,min_wait))
        lb()
        fast_print("tasks completed")
        lb()
        lb()
        input("game is ready. you are a hacker hired to break inside the evil company SORT Corporations. make sure not to lose youself in your tasks. press enter key to begin.")

        clear()

    except KeyboardInterrupt:
        clear()

def breakdown():

    sys.stdout.write(screensize)

    slow_print(">>>>>>", 0.8)

    time.sleep(0.5)

    call(['clear'])

    delay = [0.1,0.3]

    linesarray = []

    for i in range(rows):
        linesarray.append([])
        for j in range(cols):
            e = random.randint(0,1000)
            if e > 1:
                e = " "
            elif e == 0:
                    e = "♬"
            elif e == 1:
                e = "♪"
            linesarray[i].append(str(e))

    for l in linesarray:
        for c in l:
            fast_print(c)
        lb()

    time.sleep(random.uniform(delay[0],delay[1]))

    delay = [0.1,0.12]

    for c in range(10):
        for i in range(rows):
            for j in range(cols):
                if linesarray[i][j] == " ":
                    e = random.randint(0,500)
                    if e > 1:
                        e = " "
                    elif e == 0:
                            e = "♬"
                    elif e == 1:
                        e = "♪"
                    linesarray[i][j] = e

        for l in linesarray:
            for c in l:
                fast_print(c)
            lb()

        time.sleep(random.uniform(delay[0],delay[1]))
    
    
    delay = [0.1,0.15]

    for c in range(rows*4):

        clear()

        lines = []

        for i in range(rows):
            lines.append("")
            for j in range(cols):
                e = random.randint(0,4+rows-(c//4))
                if e > 1:
                    e = " "
                elif e == 0:
                    e = "♬"
                elif e == 1:
                    e = "♪"
                lines[i] += str(e)

        for l in lines:
            fast_print(l);lb();

        time.sleep(random.uniform(delay[0],delay[1]))

    for c in range(20):

        clear()

        lines = []

        for i in range(rows):
            lines.append("")
            for j in range(cols):
                e = random.randint(0,4)
                if e > 1:
                    e = " "
                lines[i] += str(e)

        for l in lines:
            fast_print(l);lb();

        time.sleep(random.uniform(delay[0],delay[1]))

def rotate():
    call(['clear'])

    sys.stdout.write(screensize)

    delay = []

    tn = get_trial_num()

    # pointer ="                    ||||"   + "\n" +
    #          "                  \¯¯__¯¯/" + "\n" +
    #          "                   \____/"  + "\n" +
    #          "                    \__/"   + "\n" +
    #          "                     \/"    + "\n" +

    pointer ="                    ||||"   + "\n" + "                  \¯¯__¯¯/" + "\n" + "                   \____/"  + "\n" + "                    \__/"   + "\n" + "                     \/"

    baredge ="------------+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+"
    baredge2="            |                   |                   |                   |                   |                   |                   |"
    barmidold = "ial" + str(tn) + "  X  |  #  trial" + str(tn+1) + "  #  |     trial" + str(tn+2) + "     |     trial" + str(tn+3) + "     |     trial" + str(tn+4) + "     |     trial" + str(tn+5) + "     |     trial" + str(tn+5) + "     |"
    barmidtrans="ial" + str(tn) + "  X  |  X  trial" + str(tn+1) + "  X  |     trial" + str(tn+2) + "     |     trial" + str(tn+3) + "     |     trial" + str(tn+4) + "     |     trial" + str(tn+5) + "     |     trial" + str(tn+5) + "     |"
    barmidnew = "ial" + str(tn) + "  X  |  X  trial" + str(tn+1) + "  X  |  #  trial" + str(tn+2) + "  #  |     trial" + str(tn+3) + "     |     trial" + str(tn+4) + "     |     trial" + str(tn+5) + "     |     trial" + str(tn+5) + "     |"

    fast_print(pointer);lb();
    fast_print(baredge[0:cols]);lb();
    fast_print(baredge2[0:cols]);lb();
    fast_print(barmidold[0:cols]);lb();
    fast_print(baredge2[0:cols]);lb();
    fast_print(baredge[0:cols]);lb();

    time.sleep(10*0.2)


    call(['clear'])

    fast_print(pointer);lb();
    fast_print(baredge[0:cols]);lb();
    fast_print(baredge2[0:cols]);lb();
    fast_print(barmidtrans[0:cols]);lb();
    fast_print(baredge2[0:cols]);lb();
    fast_print(baredge[0:cols]);lb();    

    time.sleep(10*0.2)

    for i in range(20):

        call(['clear'])

        baredge = cycle(baredge)
        baredge2 = cycle(baredge2)
        barmidold = cycle(barmidold)
        barmidtrans = cycle(barmidtrans)
        barmidnew = cycle(barmidnew)


        fast_print(pointer);lb();lb();lb();
        fast_print(baredge[0:cols]);lb();
        fast_print(baredge2[0:cols]);lb();
        fast_print(barmidtrans[0:cols]);lb();
        fast_print(baredge2[0:cols]);lb();
        fast_print(baredge[0:cols]);lb();

        time.sleep(0.2)

    call(['clear'])

    fast_print(pointer);lb();
    fast_print(baredge[0:cols]);lb();
    fast_print(baredge2[0:cols]);lb();
    fast_print(barmidtrans[0:cols]);lb();
    fast_print(baredge2[0:cols]);lb();
    fast_print(baredge[0:cols]);lb();

    time.sleep(10*0.2)

    call(['clear'])

    fast_print(pointer);lb();
    fast_print(baredge[0:cols]);lb();
    fast_print(baredge2[0:cols]);lb();
    fast_print(barmidnew[0:cols]);lb();
    fast_print(baredge2[0:cols]);lb();
    fast_print(baredge[0:cols]);lb();    

    time.sleep(20*0.2)

def end_dialogues():

    time.sleep(1.0)

    call(['clear'])
    # this will be where the story is explained, through some code-y looking stuff of course

    w = get_world()

    dt = 2 / len(w.player.name)
    slow_print("ASSAILANT: '" + w.player.name + "'",dt=0.4)

    slow_print("⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗")

    print("BREACHES:")
    for s in w.player.solved_computers:
        slow_print("[solved] " + s)

    slow_print("⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗")

    print("TRIGGERS:")
    for s in w.player.actions:
        slow_print("[completed] " + s)

    slow_print("⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗")

    print("FITNESS:")
    slow_print("[reputation] " + str(w.player.reputation))
    s = ""
    for i in w.player.inventory:
        s += str(i) + ", "
    for i in w.player.devices:
        s += str(i) + ", "
    s = s[:-2]
    slow_print("[items] " + s)

    print()
    print()
    print()
    print()

    input("[press enter to update neural net]")

    call(['clear'])
    for i in range(3):
        print("hashing neural net...")
        for j in range(rows-2):
            for k in range(cols//2):
                e = random.randint(0,1)
                if e:
                    e = "⎆-"
                else:
                    e = "  "
                fast_print(e)
                time.sleep(0.0005)
            lb()
        call(['clear'])
    
    call(['clear'])
    print("updating weights")
    for i in range(rows-2):
        for i in range(cols//2):
            e = random.randint(0,1)
            if e:
                e = "⎋^"
            else:
                e = "  "
            fast_print(e)
            time.sleep(0.002)
        lb()

    call(['clear'])

    print("trial has ended.")
    print()
    print("weights have changed significantly due to this trial:")
    print("  * this trial yeilded a high learning benefit.")
    print("  * many psychology.HUMAN attributes successfully correlated in this trial.")
    print("  * SORT has successfully identified a number of new manifest.REAL fitness.ASSAILANT.")
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    input("[press enter to unblock next trial]")

def lose():
    print("you lose :P")

def cycle(s):
    return s[1:] + s[0]

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