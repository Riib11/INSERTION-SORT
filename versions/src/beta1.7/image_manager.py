import tkinter

# open an image in a tkinter window
def open_image(name):
    name = name.replace('.png','.gif')
    name = "assets/images/" + name
    
    root = tkinter.Tk()
    image = tkinter.PhotoImage(file=name)
    tkinter.Label(root, image=image).pack()
    root.mainloop()


# from PIL import Image
# from PIL import ImageDraw

# def open_image(name):
#     Image.open("assets/images/" + name).show()