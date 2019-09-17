from Window import Window   # window class for user input
import cv2                  # opencv for reading data from images
import numpy as np          # use of multidimensional numpy arrays
import time                 # determine how efficient program is
import letter_detection     # detecting i's and j's
from Letter_Window import *
from User_Window import *
from string import ascii_lowercase


def main():

    #get_data()
    gui = User_Window()
    gui.mainloop()


def get_data():

    for i in ascii_lowercase:
        x = Letter_Window(i, 10)
        x.mainloop()


if __name__ == "__main__":
    main()


