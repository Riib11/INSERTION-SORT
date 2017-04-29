import file_manager
import image_manager
from accessor import *
import colors
import time
from debug import *
import tkintergame

# run a program that is on a game computer
def run(compname,programname):

    if programname == "impossible.xx":
        g = tkintergame.Minigame()
        try: 
            print("(game opened in new window)")
            g.play()

            if g.result == "WIN":
                print("you win!!!")
                print()
                print("{*} you gain 10000 reputation. nice skills!")
                print()
                w = get_world()
                w.player.reputation += 10000
                save_world(w)
            else:
                print("you lose :(")
            return True
            
            try:
                g.quit()
            except:
                pass

        except:
            g.quit()
            print("you lose :(")
            return True

    p = get_program(compname,programname)

    if not p:
        return False

    arg = input("enter " + p['argname'] + ": ")

    if arg in p['arg']:
        a = p['arg'][arg]

        if "loading" in a:
            colors.color_load(30,a['loading'])

        if "open" in a:
            file = a['open']
            if file == "decoy":
                colors.color_bad_load(30,file)
                print("[!] program encountered barrier; unable to complete tasks")
            if file.split(".")[1] == "txt":
                print("successfully ran program")
                file_manager.open_text(a['open'])
            elif file.split(".")[1] == "png":
                print("successfully ran program")
                image_manager.open_image(a['open'])
            else:
                colors.color_bad_load(30,0.01)
                print("[!] program unsuccessful")
                return True

        if 'message' in a:
            print(a['message'])

        if 'reputation' in a:
            w = get_world()
            print("[social] you have gained +" + str(a['reputation']) + " reputation")
            w.player.reputation += a['reputation']
            save_world(w)
        return True
    else:
        colors.color_bad_load(30,0.01)
        print("[!] invalid argument")
        return True