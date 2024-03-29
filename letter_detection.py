#
# Utility functions to be used in letter detection
#

import cv2
import numpy as np


def beautify(contours, img):

    iterate(contours, overlapping, img)
    iterate(contours, vertically_close, img)

def overlapping(c1, c2, img):

    x,y,w,h = cv2.boundingRect(c1)
    x2,y2,w2,h2 = cv2.boundingRect(c2)

    #If one rectangle is on left side of other 
    if (x > x2+w2 or x2 > x+w):
        return False 
  
    # If one rectangle is above other 
    if (y > y2+h2 or y2 > y+h): 
        return False

    
    # Area of 1st Rectangle 
    a1 = w*h
    # Area of 2nd Rectangle 
    a2 = w2*h2

    # Area of intersection    
    aI = (min(x+w, x2+w2) - max(x, x2)) *(min(y+h, y2+h2) - max(y, y2)); 

    total = (a1 + a2 - aI);

    if(a1 < a2):
        mini = a1
    else:
        mini = a2

    
    # If more than 20% of their areas intersect, they should be considered one letter
    if((aI/mini) > 0.20):
        return True

    return False



##
# Operation defines what the iteration is doing
# operation (0) => combine disjoined letters
# operation (1) => combine i's and j's
#
def iterate(contours, function, img):
    i = 0
    j = 0
    n = len(contours)
    

    # Joins contours if they are close enough vertically
    # Solves the "i" and "j" problem of the disconnected dots
    while(i < len(contours)):

        # start comparison with next in list
        # don't want to recompare objects or compare same object
        # **NOTE** -> j will always be ahead of i
        j = i + 1
        
        while(j < len(contours)):

            # check if they are close enough vertically
            copy = img.copy()

            if(function(contours[i], contours[j], img)):

                # join the two contours into one
                joined = np.concatenate((contours[i],contours[j]))
                
                # Insert our joined contour in the ith position
                # List is now original size again
                contours.append(joined)
                
                # Pop our jth contour as it is now joined
                contours.pop(j)
                contours.pop(i)

                i = -1
                j = n

            j += 1
            
        i += 1

    
def rectangle(c1, c2):
    # (x,y) is top left corner of rectangle
    # (x+w, y+h) is bottom right corner of rectangle
    #  ^y coordinates increase as you move to bottom of screen
    #  x coordinates increase as expected
    x,y,w,h = cv2.boundingRect(c1)
    x2,y2,w2,h2 = cv2.boundingRect(c2)

    # Get key points of our rectangles
    r1 = x+w
    r2 = x2+w2

    l1 = x
    l2 = x2

    top1 = y
    top2 = y2

    bot1 = y+h
    bot2 = y2+h2

    midy1 = (y + (h/2))
    midy2 = (y2 + (h2/2))
    midx1 = (x + (w/2))
    midx2 = (x2 + (w2/2))

    return r1,r2,l1,l2,top1,top2,bot1,bot2,midy1,midy2,midx1,midx2


# Essentially detects if two contours are meant to be an i or j
# Returns bool depending on if they're close enough to be considered an i or j
def vertically_close(c1, c2,img):


    r1,r2,l1,l2,top1,top2,bot1,bot2,midy1,midy2,midx1,midx2 = rectangle(c1,c2)
    # If the 2 contours are within 30 pixels of each other
    if(abs(midx1 - midx2) < 30 and (abs(r1 - (r2)) < 30 or abs((l1)-l2) < 30)):


        # if contour 1 is on bottom (i or j), and upperbound is within 65 pixels of the middle of the dot
        if((top1 > midy2) and (top1 > bot2) and ((top1 - midy2) < 65)):

            return True


        # Same as top, only contour2 is on bottom
        elif((top2>midy1) and (top2 > bot1) and (top2 - midy1)< 65):

            return True
            
        else:
            
            return False
                        
                     

    return False