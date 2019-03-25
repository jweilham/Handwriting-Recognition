from tkinter import *
import cv2
import numpy as np
from PIL import ImageGrab


###
#
#  Defines a window to draw a single letter into
#
#  Has a save, reset, and quit function on the window
#  Drawable canvas, reacts to mouse clicks
#
#  Black background and drawable area is white
#  Drawed lines are in black
#

class Window(Tk):

    
    def __init__(self):
        Tk.__init__(self)

        # Width and height of window
        self.width = 300
        self.height = 300
        
        self.drawable_width = 100
        self.drawable_height = 100


        # Initialzing window
        dimensions = str(self.width) + "x" + str(self.height)
        self.geometry(dimensions)
        self.config(bg = 'black')
        self.resizable(0,0)

        
        # Menubar for top of window
        menubar = Menu(self)
        menubar.add_command(label="Save", command=self.save)
        menubar.add_command(label="Quit!", command=self.destroy)
        self.config(menu=menubar)


        # Initializing canvas for drawable area
        self.drawing_area = Canvas(self,  bg = 'white',
                                   width = self.drawable_width,
                                   height = self.drawable_height,)
        
        self.drawing_area.pack()
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.onClick)
        self.drawing_area.bind("<ButtonRelease-1>", self.offClick)
        self.drawing_area.place(relx=0.5, rely=0.5, anchor=CENTER)


        # Member variables for implementing drawable area
        self.onClick = False
        self.previous_x = 0
        self.previous_y = 0


    # Take screenshot of drawable area
    # Save as a .TIFF for exact RGB format of 255 (white) and 0 (black)
    def save(self):

        # Subtracts and adds 2 to crop extra 2 pixels from window
        drawable_x0=self.winfo_rootx()+self.drawing_area.winfo_x()
        drawable_y0=self.winfo_rooty()+self.drawing_area.winfo_y()
        drawable_x1=drawable_x0+self.drawing_area.winfo_width()-2  
        drawable_y1=drawable_y0+self.drawing_area.winfo_height()-2
        
        ImageGrab.grab((2 + drawable_x0, 2 + drawable_y0, drawable_x1,drawable_y1)).save("plz.TIFF")


    # Triggered when user clicks, and allows line to be drawn
    def onClick(self, event):
        self.onClick = True           


    # Resets line when user lets go of the click
    def offClick(self, event):
        self.onClick = False
        self.previous_x = None
        self.previous_y = None


    # Occurs whenever user is hovering over drawable area
    def motion(self, event):

        # Creates a line from the previous position to current position
        # If dragged it appears as a smooth line in the direction they're going
        if self.onClick:
            
            if self.previous_x is not None and self.previous_y is not None:
                
                event.widget.create_line(self.previous_x, self.previous_y,
                                         event.x,         event.y,
                                         smooth=TRUE,     width = 5)
            
            self.previous_x = event.x
            self.previous_y = event.y


def main():

    w = Window();
    w.mainloop();
    image = cv2.imread("plz.TIFF")
    print (type(image))
    for i in range(image.size):
        print(image[i])

if __name__ == "__main__":
    main()
