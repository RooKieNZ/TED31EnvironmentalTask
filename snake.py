#Brad_Toase AS91907GameProto V0.1
import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW


class Cons:
    ###Constraints, overall sizing and different adjustable operands, may be used for future settings menu?###    
    BOARD_WIDTH = 300
    BOARD_HEIGHT = 300
    DELAY = 100
    DOT_SIZE = 10
    MAX_RAND_POS = 27


class Board(Canvas):

    def __init__(self):
        super().__init__(width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT,
                         background="black", highlightthickness=0)
         
        self.init_game()
        self.pack()

    def init_game(self):
        ###initializes game###

        self.inGame = True
        self.dots = 10
        
        # starting bottle coordinates
        self.bottleX = 100
        self.bottleY = 190
        
        self.load_images()

    def load_images(self):
        ###loads images from file###
        
        try:
            self.idot = Image.open("dot.png")
            self.dot = ImageTk.PhotoImage(self.idot)    
            self.ihead = Image.open("head.png")
            self.head = ImageTk.PhotoImage(self.ihead)           
            self.ibottle = Image.open("bottle.png")
            self.bottle = ImageTk.PhotoImage(self.ibottle) 

        except IOError as e:
            
            print(e)
            sys.exit(1)
        
    def create_objects(self):
        ###creates objects on Canvas###
        self.create_image(self.bottleX, self.bottleY, image=self.bottle,
                          anchor=NW, tag="bottle")
        self.create_image(50, 50, image=self.head, anchor=NW,  tag="head")
        self.create_image(30, 50, image=self.dot, anchor=NW, tag="dot")
        self.create_image(40, 50, image=self.dot, anchor=NW, tag="dot")


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

