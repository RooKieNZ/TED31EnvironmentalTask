#Brad_Toase AS91907GameProto V1

###program set to run successfully, more features to be added in future###
###dependencies and various other dohickeys###
import os
import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW

###prints all files in working directory, used to check if in correct###
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in '%s': %s" % (cwd, files))

###General perameters, such as board dimensions and turtle family speed###
class Cons:
        
    BOARD_WIDTH = 1228 #1228 just seemed like a lovely number in my head
    BOARD_HEIGHT = 1228
    DELAY = 90 
    DOT_SIZE = 68 #slightly larger size than sprite so make sure that if the image opens strangely, random differences are accounted for
    MAX_RAND_POS = 12 #amount of places bottle can spawn


class Board(Canvas):

    def __init__(self):
        super().__init__(width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT,
                         background="black", highlightthickness=0)
         
        self.init_game()
        self.pack()
	
	###stuff set when the game starts###
    def init_game(self):
		
        self.inGame = True
        self.dots = 3
        self.score = 0
        
        # variables used to move tortle object
        self.moveX = Cons.DOT_SIZE
        self.moveY = 0
        
        # starting bottle coordinates
        self.bottleX = 1000
        self.bottleY = 100
        
        self.load_images()

        #self.focus_get()
        
        self.create_objects()
        self.locate_bottle()
        self.bind_all("<Key>", self.on_key_pressed)
        self.after(Cons.DELAY, self.on_timer)

    ###loads images from file; this is using pillow, and just pulls the images from the current working directory###
    def load_images(self):
        
        try:
            self.idot = Image.open("test.png")
            self.dot = ImageTk.PhotoImage(self.idot)    
            self.ihead = Image.open("head.png")
            self.head = ImageTk.PhotoImage(self.ihead)           
            self.ibottle = Image.open("bottle.png")
            self.bottle = ImageTk.PhotoImage(self.ibottle)
        except IOError as e:
            
            print(e)
            sys.exit(1)
        
    ###creates objects on Canvas, these are then assigned different images so they may appear on screen###		
    def create_objects(self):
    
        self.create_text(30, 10, text="Score: {0}".format(self.score), 
                         tag="score", fill="white")
        self.create_image(self.bottleX, self.bottleY, image=self.bottle,
                          anchor=NW, tag="bottle")
        self.create_image(400, 100, image=self.head, anchor=NW,  tag="head")
        self.create_image(200, 100, image=self.dot, anchor=NW, tag="dot")
        self.create_image(100, 100, image=self.dot, anchor=NW, tag="dot")
    
	###checks if the head of tortle collides with bottle###
    def check_bottle_collision(self):
        bottle = self.find_withtag("bottle")
        head = self.find_withtag("head")
 
        #print(self.bbox(head))
        
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)
        
		#if turtle head hits the bottle create a new dot sprite on the head's position
        for ovr in overlap:          
            if bottle[0] == ovr:
                
                self.score += 1
                x, y = self.coords(head)
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                self.locate_bottle()

    ###moves the tortle object###
    def move_tortle(self):
          
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

    ###checks for collisions such as leaving the game border###    
    def check_collisions(self):

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")
        
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)
        
        for dot in dots:
            for over in overlap:
                if over == dot:
                    self.inGame = False
            
        if x1 < 0:
            self.inGame = False
        
        if x1 > Cons.BOARD_WIDTH - Cons.DOT_SIZE:
            self.inGame = False

        if y1 < 0:
            self.inGame = False
        
        if y1 > Cons.BOARD_HEIGHT - Cons.DOT_SIZE:
            self.inGame = False	

	###places the bottle object on Canvas at random position when called###
    def locate_bottle(self):
    
        bottle = self.find_withtag("bottle")
        self.delete(bottle[0])
    
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.bottleX = r * Cons.DOT_SIZE
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.bottleY = r * Cons.DOT_SIZE
        
        self.create_image(self.bottleX, self.bottleY, anchor=NW,
            image=self.bottle, tag="bottle")

	###controls direction variables with cursor keys###
    def on_key_pressed(self, e): 
    
        key = e.keysym
		
		#move left
        LEFT_CURSOR_KEY = "Left"
        if key == LEFT_CURSOR_KEY and self.moveX <= 0:
            
            self.moveX = -Cons.DOT_SIZE
            self.moveY = 0
        #move right
        RIGHT_CURSOR_KEY = "Right"
        if key == RIGHT_CURSOR_KEY and self.moveX >= 0:
            
            self.moveX = Cons.DOT_SIZE
            self.moveY = 0
		#move up
        UP_CURSOR_KEY = "Up"
        if key == UP_CURSOR_KEY and self.moveY <= 0:
                        
            self.moveX = 0
            self.moveY = -Cons.DOT_SIZE
		#move down
        DOWN_CURSOR_KEY = "Down"
        if key == DOWN_CURSOR_KEY and self.moveY >= 0:
            
            self.moveX = 0
            self.moveY = Cons.DOT_SIZE

	###creates a game cycle each timer event, basically a clock to update everything, would have used async option but really couldnt be bothered due to limited time###			
    def on_timer(self):

        self.draw_score()
        self.check_collisions()
		#if player in game, check where the bottle is, move the tortle and retry otherwise game is over, and dont retry
        if self.inGame:
            self.check_bottle_collision()
            self.move_tortle()
            self.after(Cons.DELAY, self.on_timer)
        else:
            self.game_over()            

	###draws score, based on the amount of times the head hits the bottle in a defined run, is then drawn in top left corner during game, and on gameover text###
    def draw_score(self):
        
        score = self.find_withtag("score")
        self.itemconfigure(score, text="Score: {0}".format(self.score))

	###deletes all objects and draws game over message###
    def game_over(self):

        self.delete(ALL)
        self.create_text(self.winfo_width() /2, self.winfo_height()/2,
                         text="Game Over with score {0}".format(self.score), fill="white")

###basically starts game, as board and pulling the main and tortle class###
class tortle(Frame):

    def __init__(self):
        super().__init__()
                
        self.master.title('tortle')
        self.board = Board()
        self.pack()


def main():

    root = Tk()
    tortle()
    root.mainloop()  


if __name__ == '__main__':
    main()

