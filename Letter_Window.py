from Window import *

# Ignore error when dividing by 0 in numpy array
np.seterr(divide='ignore', invalid='ignore')

class Letter_Window(Window):

    def __init__(self, filename, iterations = 3):
        Window.__init__(self, w = 350, h = 350, filename = filename)


        # List of data to save 
        self.dataList = []

        # number of times to collect data for letter
        self.iterations = iterations


        # Update menubar
        self.menubar.insert_command(0, label = "Submit Letter " + str(self.filename), command=self.addData)
        self.config(menu=self.menubar)

        
        self.drawing_area.config(width=200, height=200)     


    # Adds data to our save file for a specific letter
    def addData(self):

            tmpfile = "data/temporary/" + self.filename
            
            self.save(tmpfile)

            
            # Reads in our image as a numpy array
            image = cv2.imread(tmpfile+".TIFF")
            
            # make copy to not modify original image
            copy  = image.copy()

            #converts to grayscale for contour functions to work
            grayscale = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)


            # Reads in contours (outlines) of objects in image
            contours, hierarchy = cv2.findContours(grayscale,      
                                                   cv2.RETR_EXTERNAL,
                                                   cv2.CHAIN_APPROX_SIMPLE)    


            letter_detection.combine_i_j(contours)
            

            if(len(contours) > 1):
                messagebox.showerror("Error", "Please draw one letter")
                return

            

            x,y,w,h = cv2.boundingRect(contours[i])

     
            cv2.rectangle(copy,         # Draw rectangle on temporary copy
                         (x, y),        # Start
                         (x+w,y+h),     # End
                         (255, 0, 0),   # BGR value (RGB backwards)
                          2)            # Thickness       

            
            # Region of interest is our rectangle
            # Apparently our imgROI isn't read in as 0's and 255's
            # Even if we save as a .TIFF
            imgROI = image[y:y+h, x:x+w]

        
            # Resize letter to make them all in a uniform size
            # Not square because alot of letters are tall
            # Don't want to stretch them too much
            resized = cv2.resize(imgROI, (20,40))

            # Convert values to only (255,255,255) and (0,0,0)
            ones_and_nan = (resized/resized)
            binary = np.nan_to_num(ones_and_nan)
            only_white = np.multiply(255,binary)
            displayable = only_white.astype(np.uint8)
            
            self.dataList.append(displayable)

            cv2.imshow("hi", displayable)
            cv2.waitKey(0)

            feature = []
            summed = 0
            m = displayable
            for i in range(0,40,4):
                
                for j in range(0,20,4):


                    # Top left square
                    #print(i,j)
                    #print(i,j+1)
                    #print(i+1, j)
                    #print(i+1, j+1)
                    summed += m[i][j][0]
                    summed += m[i][j+1][0]
                    summed += m[i+1][j][0]
                    summed += m[i+1][j+1][0]

                    # Bottom left square
                    #print(i+2,j)
                    #print(i+2,j+1)
                    #print(i+3, j)
                    #print(i+3, j+1)
                    summed += m[i+2][j][0]
                    summed += m[i+2][j+1][0]
                    summed += m[i+3][j][0]
                    summed += m[i+3][j+1][0]
                    
                    # Top right square
                    #print(i,j+2)
                    #print(i,j+3)
                    #print(i+1, j+2)
                    #print(i+1, j+3)
                    summed += m[i][j+2][0]
                    summed += m[i][j+3][0]
                    summed += m[i+1][j+2][0]
                    summed += m[i+1][j+3][0]

                    
                    # Bottom right sqaure
                    #print(i+2,j+2)
                    #print(i+2,j+3)
                    #print(i+3, j+2)
                    #print(i+3, j+3)
                    summed += m[i+2][j+2][0]
                    summed += m[i+2][j+3][0]
                    summed += m[i+3][j+2][0]
                    summed += m[i+3][j+3][0]

                    feature.append(summed)
                    summed = 0
                    print("endSqaure\n")

                    


    
            print(np.sum(displayable))
            print(np.sum(feature)*3)
            print(feature)
                
            
            if(len(self.dataList) >= self.iterations):

                directory = "data/" + self.filename + ".npz"
                
                loaded = []
                
                try:
                    loaded = np.load(directory)
                
                except Exception as e:
                    np.savez(directory, *self.dataList)
                    print(str(e))
                    print("Created new file -> ", directory)
                    self.destroy()
                    return

                
                # Load in numpy array file
                loaded = np.load(directory)
                data = []

                # Move into a usable array
                for key in loaded:
                    data.append((loaded[key]))


                # Add new data to array
                for letter in self.dataList:
                    data.append(letter)


                # Save new data
                np.savez(directory, *data)               
                
                self.destroy()
                return



            # Clear after each letter submission
            self.clear()

