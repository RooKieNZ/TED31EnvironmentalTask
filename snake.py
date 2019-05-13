#Brad_Toase AS91907GameProto V0.5?


# dependencies and random things needed to be imported for various functionalities
import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW

# constraints, such as sizing of the board and the segments of the turtle school 
class Cons:        
    BOARD_WIDTH = 3000
    BOARD_HEIGHT = 3000
    DELAY = 100
    DOT_SIZE = 1
    MAX_RAND_POS = 27

# the board itself and general functions, such as movement, timers, score, gameplay, etc
class Board(Canvas):

# main GUI window
    def __init__(self):
        super().__init__(width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT,
                         background="black", highlightthickness=0)
         
        self.init_game()
        self.pack()

# what happens on game start, like loading sprites at certain location on screen
    def init_game(self):
        ###initializes game###

        self.inGame = True
        self.dots = 3
        self.score = 0
        
# variables used to move snake object
        self.moveX = Cons.DOT_SIZE
        self.moveY = 0
        
# starting bottle coordinates
        self.bottleX = 100
        self.bottleY = 190
        
        self.load_images()
        self.create_objects()
        self.locate_bottle()
        self.bind_all("<Key>", self.on_key_pressed)
        self.after(Cons.DELAY, self.on_timer)

# loads images from file
    def load_images(self):
# trys to open sprite files
        try:
            self.idot = Image.open("dot.png")
            self.dot = ImageTk.PhotoImage(self.idot)    
            self.ihead = Image.open("head.png")
            self.head = ImageTk.PhotoImage(self.ihead)           
            self.ibottle = Image.open("bottle.png")
            self.bottle = ImageTk.PhotoImage(self.ibottle) 
# if it cant it exits
        except IOError as e:
            print(e)
            sys.exit(1)

# creates objects on Canvas
def create_objects(self):
# places score tag in top corner, and segments of the turtle school in places, as well as the bottle they eat    
        self.create_text(30, 10, text="Score: {0}".format(self.score), 
                         tag="score", fill="white")
        self.create_image(self.bottleX, self.bottleY, image=self.bottle,
                          anchor=NW, tag="bottle")
        self.create_image(50, 50, image=self.head, anchor=NW,  tag="head")
        self.create_image(20, 50, image=self.dot, anchor=NW, tag="dot")
        self.create_image(0, 50, image=self.dot, anchor=NW, tag="dot")
   
    def check_bottle_collision(self):
# checks if the head of turtle school collides with bottle

        bottle = self.find_withtag("bottle")
        head = self.find_withtag("head")
        
        # print(self.bbox(head))
        
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)
            
        for ovr in overlap:
          
            if bottle[0] == ovr:
                
                self.score += 1
                x, y = self.coords(bottle)
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                self.locate_bottle()

    def move_snake(self):
# moves the Snake object
      
        dots = self.find_withtag("dot")
        head = self.find_withtag("head")                
        items = dots + head        
        z = 0
        while z < len(items)-1:            
            c1 = self.coords(items[z])
            c2 = self.coords(items[z+1])
            self.move(items[z], c2[0]-c1[0], c2[1]-c1[1])
            z += 1           
        self.move(head, self.moveX, self.moveY)     


    def locate_bottle(self):
# places the bottle object on Canvas at random location, then sets the sprite to the location
    
        bottle = self.find_withtag("bottle")
        self.delete(bottle[0])
    
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.bottleX = r * Cons.DOT_SIZE
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.bottleY = r * Cons.DOT_SIZE
        
        self.create_image(self.bottleX, self.bottleY, anchor=NW,
            image=self.bottle, tag="bottle")

    def on_key_pressed(self, e): 
# controls direction variables with cursor keys
    
        key = e.keysym

        LEFT_CURSOR_KEY = "Left"
        if key == LEFT_CURSOR_KEY and self.moveX <= 0:
            
            self.moveX = -Cons.DOT_SIZE
            self.moveY = 0
        
        RIGHT_CURSOR_KEY = "Right"
        if key == RIGHT_CURSOR_KEY and self.moveX >= 0:
            
            self.moveX = Cons.DOT_SIZE
            self.moveY = 0

        UP_CURSOR_KEY = "Up"
        if key == UP_CURSOR_KEY and self.moveY <= 0:
                        
            self.moveX = 0
            self.moveY = -Cons.DOT_SIZE

        DOWN_CURSOR_KEY = "Down"
        if key == DOWN_CURSOR_KEY and self.moveY >= 0:
            
            self.moveX = 0
            self.moveY = Cons.DOT_SIZE

    def on_timer(self):
# creates a game cycle each timer event

        self.draw_score()
        self.check_collisions()

        if self.inGame:
            self.check_bottle_collision()
            self.move_snake()
            self.after(Cons.DELAY, self.on_timer)
        else:
            self.game_over()            

    def draw_score(self):
# draws score on the score tag
        
        score = self.find_withtag("score")
        self.itemconfigure(score, text="Score: {0}".format(self.score))

    def game_over(self):
# deletes all objects and draws game over message

        self.delete(ALL)
        self.create_text(self.winfo_width() /2, self.winfo_height()/2,
                         text="Game Over with score {0}".format(self.score), fill="white")


class Snake(Frame):

    def __init__(self):
        super().__init__()
                
        self.master.title('Snake')
        self.board = Board()
        self.pack()


def main():

    root = Tk()
    Snake()
    root.mainloop()  


if __name__ == '__main__':
    main()

