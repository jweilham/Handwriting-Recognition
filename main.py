from Window import Window
import cv2
import numpy as np
import time


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




    imgROI = image[0:70, 0:1]
    #cv2.imshow("c1", imgROI)
    #cv2.waitKey(0)
    print(type(contours))
    
    n = len(contours)

    #for p in contours:
    #    print(p, 'AAAAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHhhh')

    i = 0
    j = 0

    
    # Contours is defined as follows ->
    
    #print("countours: ", contours)                     # Array of contours (objects) defined by arrays of points
    #print("contours[0] ", contours[0])                 # First contour (object) defined by it's array of points
    #print("contours[0][0] ", contours[0][0])           # Array of the points in the first spot of that object
    #print("contours[0][0][0] ", contours[0][0][0])     # Accessing those first points [x,y]
    #print("contours[0][0][0][0]", contours[0][0][0][0) # x value of the first point in the contour
    
    start = time.time()


    # Joins contours if they are close enough vertically
    # Solves the "i" and "j" problem of the disconnected dots
    while(i < n):

        # start comparison with next in list
        # don't want to recompare objects or compare same object
        # **NOTE** -> j will always be ahead of i
        j = i + 1
        
        while(j < n):

            #print("i: ", i, " j: ", j, "length: ", len(contours), "n: ", n)

            # check if they are close enough vertically
            # close = bool
            close = close_enough(contours[i], contours[j], copy)
            #print("CLOSE ENOUGH? : ", close)
            #print("min distance: ", close, '\n')

            if(close):
                #print("i:" , i, " j: ", j, "close! n: ", n)

   

                # join the two contours into one
                joined = np.concatenate((contours[i],contours[j]))

                # take out the original contour
                contours.pop(i)

                # Insert our joined contour in the ith position
                # List is now original size again
                contours.insert(i,joined)

                # Pop our jth contour as it is now joined
                contours.pop(j)

                # update bounds
                # check if i is 0 first
                n -= 1
                j -= 1

                if(i):
                    i -= 1

            j += 1
            
        i += 1
    

    print("--- %s seconds ---" % (time.time() - start))
    
    for obj in range(n):

        print("hello")
        #print(counter, obj)
   
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

        
        print(cv2.contourArea(contours[obj]))
        #cv2.imshow("crop", ROI_resized)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        
  
            
    cv2.imshow("rectangle", copy)


def close_enough(c1, c2, image):


    
    # (x,y) is top left corner of rectangle
    # (x+w, y+h) is bottom right corner of rectangle
    #  ^y coordinates increase as you move to bottom of screen
    #  x coordinates increase as expected
    x,y,w,h = cv2.boundingRect(c1)
    x2,y2,w2,h2 = cv2.boundingRect(c2)

    # Get key points of our rectangles
    right1 = x+w
    right2 = x2+w2

    left1 = x
    left2 = x2

    top1 = y
    top2 = y2

    bottom1 = y+h
    bottom2 = y2+h2

    middle1y = (y + (h/2))
    middle2y = (y2 + (h2/2))
    middle1x = (x + (w/2))
    middle2x = (x2 + (w2/2))

    # If the 2 contours are within 30 pixels of each other
    if(abs(middle1x - middle2x) < 30 and (abs(right1 - (right2)) < 30 or abs((left1)-left2) < 30)):


        # if contour 1 is on bottom (i or j), and upperbound is within 65 pixels of the middle of the dot
        if((top1 > middle2y) and (top1 > bottom2) and ((top1 - middle2y) < 65)):


            # if the middle of the dot is within 30 pixels of the left and right bound of c1            
            if(abs(middle2x - right1)< 30):
                return True


        # Same as top, only contour2 is on bottom
        elif((top2>middle1y) and (top2 > bottom1) and (top2 - middle1y)< 65):
            if(abs(middle1x - right2) < 30):
                return True
            
        else:
            return False
                        
                     

    return False
    
if __name__ == "__main__":
    main()
