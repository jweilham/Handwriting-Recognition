#
# Utility functions to be used in letter detection
#

import cv2
import numpy as np


def combine_i_j(contours):
    i = 0
    j = 0
    n = len(contours)
    

    # Joins contours if they are close enough vertically
    # Solves the "i" and "j" problem of the disconnected dots
    while(i < n):

        # start comparison with next in list
        # don't want to recompare objects or compare same object
        # **NOTE** -> j will always be ahead of i
        j = i + 1
        
        while(j < n):

            # check if they are close enough vertically
            if(vertically_close(contours[i], contours[j])):

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
    


# Essentially detects if two contours are meant to be an i or j
# Returns bool depending on if they're close enough to be considered an i or j
def vertically_close(c1, c2):


    
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


