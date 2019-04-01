from Window import Window   # window class for user input
import cv2                  # opencv for reading data from images
import numpy as np          # use of multidimensional numpy arrays
import time                 # determine how efficient program is
import letter_detection    # detecting i's and j's


def main():

    # Makes window for letter a
    w = Window("a");
    w.mainloop();

    # Reads in our image as a numpy array
    image = cv2.imread("a.TIFF")


    # make copy to not modify original image
    copy  = image.copy()

    
    #converts to grayscale for contour functions to work
    grayscale = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)


    # Reads in contours (outlines) of objects in image
    contours, hierarchy = cv2.findContours(grayscale,      
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)    



    # Contours are defined as follows ->
    
    #print("countours: ", contours)                     # Array of contours (objects) defined by arrays of points
    #print("contours[0] ", contours[0])                 # First contour (object) defined by it's array of points
    #print("contours[0][0] ", contours[0][0])           # Array of the points in the first spot of that object
    #print("contours[0][0][0] ", contours[0][0][0])     # Accessing those first points [x,y]
    #print("contours[0][0][0][0]", contours[0][0][0][0) # x value of the first point in the contour

    
    start = time.time()

    letter_detection.combine_i_j(contours)
    
    
    print("--- %s seconds ---" % (time.time() - start))
    
    for obj,c in enumerate(contours):

        x,y,w,h = cv2.boundingRect(contours[obj])

 
        cv2.rectangle(copy,         # Draw rectangle on temporary copy
                     (x, y),        # Start
                     (x+w,y+h),     # End
                     (255, 0, 0),   # BGR value (RGB backwards)
                      2)            # Thickness       

        
        # Region of interest is our rectangle
        imgROI = image[y:y+h, x:x+w]

    
        # Resize?
        ROI_resized = cv2.resize(imgROI, (30, 50))


            
    cv2.imshow("rectangle", copy)



    
if __name__ == "__main__":
    main()
