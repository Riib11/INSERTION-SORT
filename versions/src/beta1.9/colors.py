import sys
import time

# cool printing using color formatting!
def color_print(txt,c1=1,c2=11):
    code = str(c1 * 16 + c2)
    sys.stdout.write(u"\u001b[48;5;" + code + "m" + str(txt))
    sys.stdout.flush()

# turn back to normal color
def stop_color():
    print(u"\u001b[0m")

# a cool loading bar effect, used for programs to run
def color_load(max,dt):
    for i in range(max):
        color_print(" ",15,15)
        time.sleep(dt)
    stop_color()

# a program will sometime work incorrectly, and then this will run
def color_bad_load(max,dt):
    end = max // 3
    for i in range(max-end):
        color_print(" ",15,15)
        time.sleep(dt)
    for i in range(end):
        color_print(" ",0,1)
        time.sleep(dt*10)
    stop_color()