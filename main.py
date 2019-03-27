from Window import Window
import cv2
import numpy as np
import time


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




    
    print(type(contours))
    '''
    print(contours[0])
    contours[0].sort(axis=2)
    print(contours[0])
    print(contours[0][0][0][0],contours[0][0][0][1])
    '''
    
    n = len(contours)

    #for p in contours:
    #    print(p, 'AAAAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHhhh')

    i = 0
    j = 0

    

    
    start = time.time()


    # Joins contours if they are close enough vertically
    # Solves the "i" and "j" problem of the disconnected dots
    while(i < n):

        j = i + 1
        while(j < n):

            #print("i: ", i, " j: ", j, "length: ", len(contours), "n: ", n)
            close = distance(contours[i], contours[j])
            #print("min distance: ", close, '\n')


            
            if(close):
                #print("i:" , i, " j: ", j, "close! n: ", n)


                # Probably clean up the logic here later
                # Takes out the two contours and joins them
                # reinserts joined contour back into the list
                joined = np.concatenate((contours[i],contours[j]))
                contours.pop(i)
                contours.insert(i,joined)
                contours.pop(j)

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


def distance(c1, c2):

    mind = 9999999999

    n1 = len(c1)
    n2 = len(c2)
    
    for i in range(n1):

        for j in range (n2):

            #print("c1: ", c1)
            #print("c2: ", c2)
            diffx = 5*abs(c1[i][0][0] - c2[j][0][0])
            diffy = abs(c1[i][0][1] - c2[j][0][1])
            dist =  diffy + diffx 

            #print("diffy: " , diffy, " diffx: ", diffx)
            
            if(dist < mind):
                mind = dist
                #print("adjusted distance: ", mind)
                #print("x1: ", c1[i][0][0], " x2: ", c2[j][0][0])
                #print("y1 ", c1[i][0][1], " y2: ", c2[j][0][1])
                #print("diffy: " , diffy, " diffx: ", diffx)

                if(mind < 30):

                    return True
                
    '''if(mind < 50):
        print("min distance: ", mind)
        print("c1 area: ", cv2.contourArea(c1), " c2 area: ", cv2.contourArea(c2))
        return True
    '''
    return False
    


if __name__ == "__main__":
    main()
