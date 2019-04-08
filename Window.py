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
    def __init__(self, w = 700, h = 700, filename = "user_input", train = False):
        Tk.__init__(self)


        # Menubar for top of Window
        menubar = Menu(self)

        if(train):
            menubar.add_command(label = "Submit for Training", command=self.train)
            self.width = 500
            self.height = 500
            self.drawable_width = 200
            self.drawable_height = 200

            self.trainingList = []

        else:
        

            menubar.add_command(label = "Save & Quit", command=self.saveq)



            self.width = w
            self.height = h
            self.drawable_width = w - 20
            self.drawable_height = h - 20

        menubar.add_command(label = "Pen", command=(self.onPen))
        menubar.add_command(label = "Eraser", command=(self.onEraser))
        menubar.add_command(label = "Undo (drawing)", command=(self.undo))        
        menubar.add_command(label = "Clear", command=self.clear)

        
        # Where to save the image (as a .TIFF)
        self.filename = str(filename)
        


        # Initialzing window        
        dimensions = str(self.width) + "x" + str(self.height)
        self.geometry(dimensions)
        self.config(bg = 'white')
        self.resizable(0,0)

        

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
    def save(self):

        # Subtracts and adds 2 to crop extra 2 pixels from window
        drawable_x0=self.winfo_rootx()+self.drawing_area.winfo_x()
        drawable_y0=self.winfo_rooty()+self.drawing_area.winfo_y()
        drawable_x1=drawable_x0+self.drawing_area.winfo_width()-2  
        drawable_y1=drawable_y0+self.drawing_area.winfo_height()-2
        
        ImageGrab.grab((2 + drawable_x0, 2 + drawable_y0,
                            drawable_x1,     drawable_y1)).save(self.filename+".TIFF")

    



            

    def saveq(self):
        self.save()
        self.destroy()
        
    def undo(self):
            
        if(len(self.previous_moves)):
            
            undo = self.previous_moves[self.clicks]

            for obj in undo:
                
                self.drawing_area.create_line(obj[0], obj[1],
                                             obj[2],  obj[3],
                                             smooth=TRUE,     width = obj[4], fill = obj[5])

    
            self.previous_moves.pop(self.clicks)
            self.clicks -= 1

        # end if
            
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
                    


    def train(self):

            self.save()
            
            # Reads in our image as a numpy array
            image = cv2.imread(self.filename+".TIFF")
            
            # make copy to not modify original image
            copy  = image.copy()

            #converts to grayscale for contour functions to work
            grayscale = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)


            # Reads in contours (outlines) of objects in image
            contours, hierarchy = cv2.findContours(grayscale,      
                                                   cv2.RETR_EXTERNAL,
                                                   cv2.CHAIN_APPROX_SIMPLE)    

            
       

            letter_detection.combine_i_j(contours)
            
            


            if(len(contours) != 1):
                messagebox.showerror("Error", "Please draw one letter")
                return
            
            for i in range(len(contours)):

                x,y,w,h = cv2.boundingRect(contours[i])

         
                cv2.rectangle(copy,         # Draw rectangle on temporary copy
                             (x, y),        # Start
                             (x+w,y+h),     # End
                             (255, 0, 0),   # BGR value (RGB backwards)
                              2)            # Thickness       

                
                # Region of interest is our rectangle
                # Apparently our imgROI isn't read in as 0's and 255's
                # Even if we save as a .TIFF
                imgROI = image[y:y+h, x:x+w]

            
                # resize image to 30x50 to make a uniform size
                # 30x50 because alot of letters are tall
                # don't want to stretch them too much
                resized = cv2.resize(imgROI, (30, 50))
                binary = resized/resized
                self.trainingList.append(binary)
            
            
            if(len(self.trainingList) > 2):
                a1 = self.trainingList[0]
                a2 = self.trainingList[1]
                a3 = self.trainingList[2]

                for i in range(len(self.trainingList)):
                    print(self.trainingList[i])
                np.savez("data/" + self.filename, one = a1, two = a2, three = a3)


                l = np.load('data/a.npz')


                print(np.array_equal(self.trainingList[0],l['one']))
                print(np.array_equal(self.trainingList[1],l['two']))
                print(np.array_equal(self.trainingList[2],l['three']))
                print(np.array_equal(self.trainingList[0],l['two']))
                                        
                #print("LOADED")
                #print(l['one'])
                #print(l['two'])
                #print(l['three'])
                self.destroy()
                return
        
            self.clear()
