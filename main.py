from Window import Window   # window class for user input
import cv2                  # opencv for reading data from images
import numpy as np          # use of multidimensional numpy arrays
import time                 # determine how efficient program is
import letter_detection     # detecting i's and j's
from Letter_Window import *
from User_Window import *
from string import ascii_lowercase

def main():


    get_alphabet()

    

    name = None
    
    #print(type(name))
            
    t = Letter_Window("b")
    t.mainloop()

    u = User_Window()
    u.mainloop()

    b = np.load("./data/features/b.npz")

    bs = []
    for key in b:
        bs.append(b[key])

    print(len(bs))

    

def get_alphabet():

    for i in ascii_lowercase:
        print(i)
        #data = Letter_Window(i)
        #data.mainloop()
        
if __name__ == "__main__":
    main()
