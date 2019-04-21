from Window import *


class User_Window(Window):


    def __init__(self):
        Window.__init__(self, w = 700, h = 500)
        
	# Update menubar
        self.menubar.insert_command(0, label = "Save & Quit", command=self.saveq)
        self.menubar.insert_command(0, label = "Use last input", command=self.last)
        self.config(menu=self.menubar)



    def saveq(self):
        
        self.save("user_input/" + self.filename)
        self.display()


    def last(self):
        
        self.display()

    def display(self):
        # Reads in our image as a numpy array
        image = cv2.imread("user_input/" + self.filename + ".TIFF")
        
        # make copy to not modify original image
        copy  = image.copy()

        #converts to grayscale for contour functions to work
        grayscale = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)

        # Reads in contours (outlines) of objects in image
        contours, hierarchy = cv2.findContours(grayscale,      
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE  )    

        letter_detection.combine_i_j(contours, copy)
        
        for i in range(len(contours)):
            
            x,y,w,h = cv2.boundingRect(contours[i])
     
            cv2.rectangle(copy,         # Draw rectangle on temporary copy
                         (x, y),        # Start
                         (x+w,y+h),     # End
                         (255, 0, 0),   # BGR value (RGB backwards)
                          2)            # Thickness       


        self.destroy()
        cv2.imshow("user_input", copy)
        cv2.waitKey(0)
