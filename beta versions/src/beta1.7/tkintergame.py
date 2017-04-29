from tkinter import *
import time
import random
import math
random.seed()

"""
A fun and challenging minigame on Larry's and Talos's computers.
You are a ball flying along trying to dodge spinning leaf-shaped projectiles
Try to get to the end! (fill up the green progress bar along the top of the screen)
"""
class Minigame:
    def __init__(self):
        self.result = None

        self.root = Tk()

        self.root.title("IMPOSSIBLE GAME")

        # green progressbar tracks how far along you are
        self.progressbar = Canvas(self.root, height=10, width=300)
        self.progressbar.pack()
        self.total = 1000

        self.canvas = Canvas(self.root, height=300, width=300, bd=3)
        self.canvas.pack()

        self.bullets = []

        self.current = 150
        self.s = 0
        self.size = 10

        self.root.bind("<space>", self.jump)

        # root.pack()
        self.root.resizable(width=False, height=False)

        self.counter = 0

        self.end = False

    def get_progress(self):
        return self.counter / self.total

    def update_progress(self):
        self.counter += 1
        self.progressbar.delete("all")
        self.progressbar.create_rectangle(0,0,int(self.get_progress()*300),20,fill="green")

    def play(self):
        Button(self.root, text="Start", command=self.update).pack()
        Label(self.root, text="(spacebar to control)").pack()

        self.root.mainloop()
    
    def quit(self):
        self.root.quit()
        self.root.destroy() 

    def jump(self,evt):
        if len(self.bullets) != 0:
            self.s += -5

    def lose(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0,0,300,300,fill="blue")
        self.canvas.create_text(150,150,justify=CENTER,text="LOSE!",fill="red")
        self.root.update()
        self.result = "LOSE"
        self.end = True

        self.root.after(700,self.quit)

    def win(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0,0,300,300,fill="green")
        self.canvas.create_text(150,150,justify=CENTER,text="WIN!",fill="blue")
        self.root.update()
        self.result = "WIN"
        self.end = True

        self.root.after(700,self.quit)

    def update(self,evt=None):
        if self.counter > self.total and not self.end:
            self.win()
            self.update()
        elif not self.end:

            # move player according to speed
            self.current += self.s

            if self.current < 0 or self.current > 300:
                self.lose()
                self.update()

            # draw player
            self.canvas.delete("all")
            self.canvas.create_oval(20-self.size, self.current-self.size , 20+self.size, self.current+self.size, fill="blue")

            # add bullet
            r = random.randint(0,20)
            if r < 3:
                self.bullets.append(Bullet(self.canvas))

            it = self.bullets[:]
            for b in self.bullets:
                b.draw()
                if not b.in_bounds():
                    self.bullets.remove(b)

            # see if collide with player
            if any(b.collide(20,self.current) == True for b in self.bullets):
                self.lose()
                self.update()

            # check for collisions
            
            # accelerate downward
            self.s += 0.1

            self.root.update()

            self.update_progress()

            def safe_update():
                try:
                    self.update()
                except:
                    pass

            self.root.after(20, safe_update)

        else:
            self.update()

class Bullet:
    def __init__(self, canvas):
        self.y = random.randint(10,300-10)
        self.x = 300-10
        self.size = 10
        self.canvas = canvas
        self.deg = 0

    def corner_x(self,n):
        add = n * math.pi/4
        return self.x + (self.size * math.cos(self.deg + add))

    def corner_y(self,n):
        add = n * math.pi/4
        return self.y + (self.size * math.sin(self.deg + add))

    def draw(self):
        # draw
        self.canvas.create_polygon(
                    self.corner_x(0),
                    self.corner_y(0),
                    self.corner_x(1),
                    self.corner_y(1),
                    self.corner_x(2),
                    self.corner_y(2),
                    self.corner_x(3),
                    self.corner_y(3),
                    fill="red")
        # move
        self.x -= 5

        # rotate
        self.deg += math.pi/12



    def collide(self,x,y):
        if abs(self.x - x) < self.size and abs(self.y - y) < self.size:
            return True
        return False

    def in_bounds(self):
        return self.x > 0

# mg = Minigame()
# mg.play()
# print(mg.result)