from Window import Window   # window class for user input
import cv2                  # opencv for reading data from images
import numpy as np          # use of multidimensional numpy arrays
import time                 # determine how efficient program is
import letter_detection     # detecting i's and j's
from Letter_Window import *
from User_Window import *
from string import ascii_lowercase


def alphabet():

    for i in ascii_lowercase:
        data = []
        load = np.load("./data/features/" + i + ".npz")

        j = 0
        for key in load:
            data.append(load[key])
            print(i, data[j])
            j+=1

    
def main():

    #alphabet()

    y = Letter_Window("y", 50)
    y.mainloop()


    for i in ascii_lowercase:
        print(i)
        #data = Letter_Window(i)
        #data.mainloop()
        
if __name__ == "__main__":
    main()


