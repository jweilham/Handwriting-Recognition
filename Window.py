from tkinter import *       # GUI and drawable canvas
import cv2                  # Reading in a TIFF image
import numpy as np          # RGB array
from PIL import ImageGrab   # Screenshot to convert drawn image


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


    # Constructor
    # Takes in filename to save for the image (Will automatically add .TIFF to filename)
    def __init__(self, filename):
        Tk.__init__(self)

        # Sizes of window and canvas
        self.width = 700
        self.height = 700
        self.drawable_width = 605
        self.drawable_height = 600


        # Where to save the image (as a .TIFF)
        self.filename = str(filename)


        # Initialzing window        
        dimensions = str(self.width) + "x" + str(self.height)
        self.geometry(dimensions)
        self.config(bg = 'white')
        self.resizable(0,0)

        
        # Menubar for top of window
        menubar = Menu(self)
        menubar.add_command(label="Save", command=self.save)
        menubar.add_command(label = "Clear", command=self.clear)
        menubar.add_command(label="Quit!", command=self.destroy)
        self.config(menu=menubar)


        # Initializing canvas for drawable area
        self.drawing_area = Canvas(self,  bg = 'black',
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
        
        ImageGrab.grab((2 + drawable_x0, 2 + drawable_y0,
                            drawable_x1,     drawable_y1)).save(self.filename + ".TIFF")
       
    def clear(self):
        self.drawing_area.delete("all") 

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
            if self.previous_x and self.previous_y:               
                event.widget.create_line(self.previous_x, self.previous_y,
                                         event.x,         event.y,
                                         smooth=TRUE,     width = 5, fill = 'white')
                
            self.previous_x = event.x
            self.previous_y = event.y

