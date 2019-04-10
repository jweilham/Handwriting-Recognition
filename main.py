from Window import Window   # window class for user input
import cv2                  # opencv for reading data from images
import numpy as np          # use of multidimensional numpy arrays
import time                 # determine how efficient program is
import letter_detection     # detecting i's and j's
from Letter_Window import *
from User_Window import *
from string import ascii_uppercase

def main():


    get_alphabet()
    # Makes window for letter a

    t = Letter_Window("b")
    t.mainloop()

    u = User_Window()
    u.mainloop()
    


def get_alphabet():

    for i in ascii_uppercase:
        data = Letter_Window(i)
        data.mainloop()
        
if __name__ == "__main__":
    main()
