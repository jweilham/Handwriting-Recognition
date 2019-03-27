from Window import Window
import cv2
import numpy as np



#  Look into joining contours that are near
#
#

def main():

    # Makes window for letter a
    w = Window("a");
    w.mainloop();

    # Reads in our image as an array
    image = cv2.imread("a.TIFF")

    copy  = image.copy()
    
    #converts to grayscale for contour functions to work
    grayscale = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)

    # Reads in contours (outlines) of objects in image
    contours, hierarchy = cv2.findContours(grayscale,      
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)    




    print(len(contours))

    counter  = 0
    for obj in contours:
        counter += 1
        
        #print(counter, obj)
   
        x,y,w,h = cv2.boundingRect(obj)

 
        cv2.rectangle(copy,         # Draw rectangle on temporary copy
                     (x, y),        # Start
                     (x+w,y+h),     # End
                     (255, 0, 0),   # BGR value (RGB backwards)
                      2)            # Thickness       

        # Region of interest is our rectangle
        imgROI = image[y:y+h, x:x+w]

        # Resize?
        ROI_resized = cv2.resize(imgROI, (30, 30))

        
        print(cv2.contourArea(obj))
        cv2.imshow("crop", ROI_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    cv2.imshow("rectangle", copy)



if __name__ == "__main__":
    main()
