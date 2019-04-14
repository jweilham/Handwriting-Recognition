from tkinter import *       # GUI and drawable canvas
import cv2                  # Reading in a TIFF image
import numpy as np          # RGB array
from PIL import ImageGrab   # Screenshot to convert drawn image
import letter_detection
from tkinter import messagebox

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
    def __init__(self, w = 500, h = 500, filename = "user_input"):
        Tk.__init__(self)

        
        # Menubar for top of Window
        self.menubar = Menu(self)
        

        #self.menubar.add_command(label = "Save & Quit", command=self.saveq)

        self.width = w
        self.height = h
        self.drawable_width = w - 20
        self.drawable_height = h - 20

        self.menubar.add_command(label = "Pen", command=(self.onPen))
        self.menubar.add_command(label = "Eraser", command=(self.onEraser))
        self.menubar.add_command(label = "Undo (drawing)", command=(self.undo))        
        self.menubar.add_command(label = "Clear", command=self.clear)
        self.config(menu=self.menubar)

        self.bind("<Return>")
        
        # Where to save the image (as a .TIFF)
        self.filename = str(filename)
        

        # Initialzing window        
        dimensions = str(self.width) + "x" + str(self.height)
        self.geometry(dimensions)
        self.config(bg = 'white')
        self.resizable(0,0)
        

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
        self.eraser = False

    
        # Functions as stack to allow for undo of last drawing
        # Number of clicks is top of stack
        self.previous_moves = []
        self.clicks = -1

        # Array of lines that were drawn
        self.last_move = []

        # Keeps track of if we actually drew a line last click
        self.drew = False

        
    # Take screenshot of drawable area
    # Save as a .TIFF for exact RGB format of 255 (white) and 0 (black)
    def save(self, filename):

        # Subtracts and adds 2 to crop extra 2 pixels from window
        drawable_x0=self.winfo_rootx()+self.drawing_area.winfo_x()
        drawable_y0=self.winfo_rooty()+self.drawing_area.winfo_y()
        drawable_x1=drawable_x0+self.drawing_area.winfo_width()-2  
        drawable_y1=drawable_y0+self.drawing_area.winfo_height()-2
        
        ImageGrab.grab((2 + drawable_x0, 2 + drawable_y0,
                            drawable_x1,     drawable_y1)).save(filename+".TIFF")


    def undo(self):
            
        if(len(self.previous_moves)):
            
            undo = self.previous_moves[self.clicks]

            for obj in undo:
                
                self.drawing_area.create_line(obj[0], obj[1],
                                             obj[2],  obj[3],
                                             smooth=TRUE,     width = obj[4], fill = obj[5])

    
            self.previous_moves.pop(self.clicks)
            self.clicks -= 1

            
    def clear(self):
        self.drawing_area.delete("all")
        self.previous_moves.clear()
        self.last_move.clear()
        self.clicks = -1

        
    def onClick(self, event):
        self.onClick = True


    def onEraser(self):
        self.eraser = True


    def onPen(self):
        self.eraser = False


    # Resets line when user lets go of the click
    def offClick(self, event):
        self.onClick = False
        self.previous_x = None
        self.previous_y = None

        # If we drew a line last time
        # Base case: clicking and not moving mouse
        if(self.drew):
            
            # Append to list by value, not by reference
            self.previous_moves.append(list(self.last_move))
            self.last_move.clear()
            self.clicks += 1


    # Occurs whenever user is hovering over drawable area
    def motion(self, event):

        # Creates a line from the previous position to current position
        # If dragged it appears as a smooth line in the direction they're going
        if self.onClick:

            # If our previous position exists
            if self.previous_x and self.previous_y:


                # Detect whether we are erasing or drawing
                if(self.eraser):
                    event.widget.create_line(self.previous_x, self.previous_y,
                         event.x,         event.y,
                         smooth=TRUE,     width = 20, fill = 'black')
                    self.drew = False
                    
                else:
                    
                    event.widget.create_line(self.previous_x, self.previous_y,
                                             event.x,         event.y,
                                             smooth=TRUE,     width = 5, fill = 'white')
                    
                    self.last_move.append([self.previous_x, self.previous_y, event.x, event.y, 5, 'black'])
                    self.drew = True


            # Update our previous postion with our current position
            self.previous_x = event.x
            self.previous_y = event.y
            
        else:
            
            self.drew = False
                    

