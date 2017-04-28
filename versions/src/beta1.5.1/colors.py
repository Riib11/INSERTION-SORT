import sys
import time

def color_print(txt,c1=1,c2=11):
    code = str(c1 * 16 + c2)
    sys.stdout.write(u"\u001b[48;5;" + code + "m" + str(txt))
    sys.stdout.flush()

def stop_color():
    print(u"\u001b[0m")

def color_load(max,dt):
    for i in range(max):
        color_print(" ",15,15)
        time.sleep(dt)
    stop_color()

def color_bad_load(max,dt):
    end = max // 3
    for i in range(max-end):
        color_print(" ",15,15)
        time.sleep(dt)
    for i in range(end):
        color_print(" ",0,1)
        time.sleep(dt*10)
    stop_color()