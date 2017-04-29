import time
import sys

# open a text file, and print the contents
def open_text(name):
    print("opening...")
    print()
    
    if name.split(".")[1] == "email":
        name = name.split(".")[0] + ".txt"

    with open("assets/text/" + name, "r") as file:
        slow_print(file.read())
    print()


# printing utility
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