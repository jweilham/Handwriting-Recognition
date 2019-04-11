from Window import Window   # window class for user input
import cv2                  # opencv for reading data from images
import numpy as np          # use of multidimensional numpy arrays
import time                 # determine how efficient program is
import letter_detection     # detecting i's and j's
from Letter_Window import *
from User_Window import *
from string import ascii_uppercase

def main():


    #get_alphabet()

    
    for i in range(0,40,4):
        print(i)
        for j in range(0,20,4):
            # Top left square
            print(i,j)
            print(i,j+1)
            print(i+1, j)
            print(i+1, j+1)

            # Bottom left square
            print(i+2,j)
            print(i+2,j+1)
            print(i+3, j)
            print(i+3, j+1)

            # Top right square
            print(i,j+2)
            print(i,j+3)
            print(i+1, j+2)
            print(i+1, j+3)

            # Bottom right sqaure
            print(i+2,j+2)
            print(i+2,j+3)
            print(i+3, j+2)
            print(i+3, j+3)
            print("endSqaure\n")


        

    
            
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
