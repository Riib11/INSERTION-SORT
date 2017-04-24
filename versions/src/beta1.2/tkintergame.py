from tkinter import *
import time
import random
random.seed()

class Minigame:
    def __init__(self):
        self.result = None

        self.root = Tk()

        self.root.title("IMPOSSIBLE GAME")

        self.canvas = Canvas(self.root, height=300, width=300)
        self.canvas.pack()

        self.bullets = []

        self.current = 150
        self.s = 0
        self.size = 10

        self.root.bind("<space>", self.jump)

        # root.pack()
        self.root.resizable(width=False, height=False)

        self.counter = 0

    def play(self):
        Button(self.root, text="Start", command=self.update).pack()

        self.root.mainloop()
    
    def quit(self):
        self.root.quit()
        self.root.destroy() 

    def jump(self,evt):
        self.s += -5

    def update(self,evt=None):
        if self.counter > 1000:
            self.result = "WIN"
            self.quit()

        try:
            # move player according to speed
            self.current += self.s

            if self.current < 0:
                self.result = "LOSE"
                self.quit()
            elif self.current > 300:
                self.result = "LOSE"
                self.quit()

            # draw player
            self.canvas.delete("all")
            self.canvas.create_oval(20-self.size, self.current-self.size , 20+self.size, self.current+self.size, fill="blue")

            # add bullet
            r = random.randint(0,20)
            if r < 3:
                self.bullets.append(Bullet(self.canvas))

            for b in self.bullets:
                b.draw()

            # see if collide with player
            if any(b.collide(20,self.current) == True for b in self.bullets):
                self.result = "LOSE"
                self.quit()

            # check for collisions
            
            # accelerate downward
            self.s += 0.1

            self.root.update()
            time.sleep(0.01)

            self.counter += 1

            self.update()
        except:
            pass

class Bullet:
    def __init__(self, canvas):
        self.y = random.randint(10,300-10)
        self.x = 300-10
        self.size = 10
        self.canvas = canvas

    def draw(self):
        # draw
        self.canvas.create_rectangle(self.x-self.size,self.y-self.size,self.x+self.size,self.y+self.size, fill="red")
        # move
        self.x -= 5

    def collide(self,x,y):
        if abs(self.x - x) < self.size/2 and abs(self.y - y) < self.size/2:
            return True
        return False