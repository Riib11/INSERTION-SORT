import file_manager
import image_manager
from accessor import *
import colors
from debug import *
import tkintergame

def run(compname,programname):

    if programname == "impossible.xx":
        try: 
            g = tkintergame.Minigame()
            g.play()

            if g.result == "WIN":
                print("you win!!!")
            else:
                print("you lose :(")
        except:
            print("you lose :(")




    p = get_program(compname,programname)

    if not p:
        return False

    arg = input("enter " + p['argname'] + ": ")

    if arg in p['arg']:
        a = p['arg'][arg]

        if "open" in a:
            file = a['open']
            if file == "decoy":
                colors.color_bad_load(30,file)
                print("[!] program encountered barrier; unable to complete tasks")
            if file.split(".")[1] == "txt":
                if "loading" in a:
                    colors.color_load(30,a['loading'])
                print("successfully ran program")
                file_manager.open_text(a['open'])
            elif file.split(".")[1] == "png":
                if "loading" in a:
                    colors.color_load(30,a['loading'])
                print("successfully ran program")
                image_manager.open_image(a['open'])
            else:
                print("[!] program unsuccessful")
                return False

        if 'message' in a:
            print(a['message'])

        if 'reputation' in a:
            w = get_world()
            print("[social] you have gained +" + str(a['reputation']) + " reputation")
            w.player.reputation += a['reputation']
            save_world(w)
        return True
    else:
        print("[!] invalid argument")
        return False