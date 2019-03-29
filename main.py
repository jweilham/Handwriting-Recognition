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
    cv2.imshow("c1", imgROI)
    cv2.waitKey(0)
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
            close = close_enough(contours[i], contours[j], image)
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
        cv2.imshow("crop", ROI_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        
  
            
    cv2.imshow("rectangle", copy)


def close_enough(c1, c2, image):

    minimum_distance = 9999999999

    n1 = len(c1)
    n2 = len(c2)

    c1x = 99999
    c1y = 99999

    c2x = 0
    c2y = 0
    
    M1 = cv2.moments(c1)
    if(int(M1['m00'])):
        
        c1x = int(M1['m10']/M1['m00'])
        c1y = int(M1['m01']/M1['m00'])

    M2 = cv2.moments(c2)
    if(int(M2['m00'])):
        c2x = int(M2['m10']/M2['m00'])
        c2y = int(M2['m01']/M2['m00'])
    
    leftmost1 = tuple(c1[c1[:,:,0].argmin()][0])
    rightmost1 = tuple(c1[c1[:,:,0].argmax()][0])
    topmost1 = tuple(c1[c1[:,:,1].argmin()][0])
    bottommost1 = tuple(c1[c1[:,:,1].argmax()][0])

    leftmost2 = tuple(c2[c2[:,:,0].argmin()][0])
    rightmost2 = tuple(c2[c2[:,:,0].argmax()][0])
    topmost2 = tuple(c2[c2[:,:,1].argmin()][0])
    bottommost2 = tuple(c2[c2[:,:,1].argmax()][0])

    
    x,y,w,h = cv2.boundingRect(c1)
    imgROI = image[0:70, 0:1]
    #cv2.imshow("c1", imgROI)
    #cv2.waitKey(0)


    x,y,w,h = cv2.boundingRect(c2)
    imgROI = image[y:y+h, x:x+w]
    #cv2.imshow("c2", imgROI)
    #cv2.waitKey(0)
    
    cv2.destroyAllWindows()
    if((abs((abs(c1x-c2x) - abs(c1y-c2y))) < 150)):

        if(((abs(topmost1[1] - bottommost2[1]) < 70) or (abs(bottommost1[1] - topmost2[1]) < 70))):
               
            for i in range(n1):

                for j in range (n2):

                    # Add more weight to horizontal distance
                    # Don't want to join letters that are next to each other
                    diff_x = 10*abs(c1[i][0][0] - c2[j][0][0])
                    diff_y = abs(c1[i][0][1] - c2[j][0][1])
                    
                    dist =  diff_x + diff_y 

                    #print("diffy: " , diff_y, " diffx: ", diff_x)


                    if(dist < minimum_distance): 

                        minimum_distance = dist
                        #print("min dist: ", minimum_distance)

                        if(minimum_distance < 60): 
                            
                            return True
                        
                     

    return False
    
if __name__ == "__main__":
    main()
