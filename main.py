from Window import Window   # window class for user input
import cv2                  # opencv for reading data from images
import numpy as np          # use of multidimensional numpy arrays
import time                 # determine how efficient program is
import letter_detection     # detecting i's and j's


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
    
    for c,obj in enumerate(contours):

        x,y,w,h = cv2.boundingRect(contours[c])

 
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



        # Divide array by itself in order turn it into 0's and 1's
        # 1's being the white space, and 0's being the black space
        # numpy adds in "nan" for 0/0 division for not a number (can be ignored)
        adjusted = resized/resized

        Sum = 0
        for i in adjusted:
            Sum += np.nansum(i)

    
        print(type(adjusted))

        print(adjusted)




        print(type(Sum))


        print(Sum)
        
        
        cv2.imshow("resized" + str(c), resized)



            
    cv2.imshow("rectangle", copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    
if __name__ == "__main__":
    main()
