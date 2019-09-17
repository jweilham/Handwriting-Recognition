from Window import *
import os, os.path

# Ignore error when dividing by 0 in numpy array
np.seterr(divide='ignore', invalid='ignore')

class Letter_Window(Window):

    def __init__(self, filename, iterations = 3):
        Window.__init__(self, w = 350, h = 350, filename = filename)


        self.bind("<Return>", lambda e:self.addData())
        # List of data to save 
        #self.dataList = []
        self.features = []

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
            image = cv2.imread(tmpfile + ".TIFF")
            
            # make copy to not modify original image
            copy  = image.copy()

            #converts to grayscale for contour functions to work
            grayscale = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)

            # dilate (expand) contours by 2 pixels
            kernel = np.ones((2,2),np.uint8)
            dilation = cv2.dilate(grayscale,kernel,iterations = 1)

            # Join contours that are close enough by a 9x30 rectangle
            rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 30))
            dilated = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, rect_kernel)

            #cv2.imshow("dialated", dilated)
            #cv2.waitKey(0)
        
            
            contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            
            letter_detection.beautify(contours, copy)


            if(len(contours) > 1):
                messagebox.showerror("Error", "Please draw one letter")
                return

            
            
            x,y,w,h = cv2.boundingRect(contours[0])

     
            cv2.rectangle(copy,         # Draw rectangle on temporary copy
                         (x, y),        # Start
                         (x+w,y+h),     # End
                         (255, 0, 0),   # BGR value (RGB backwards)
                          2)            # Thickness       

            

            imgROI = image[y:y+h, x:x+w]

            new_feature = self.get_feature(imgROI)
            
            self.features.append(new_feature)
            
            if(len(self.features) >= self.iterations):

                img_dir = "data/images/" + self.filename + ".npz"
                feature_dir = "data/features/" + self.filename + ".npz"
                
                loaded_images = []
                loaded_features = []
                
                try:
                    
                    img_data = np.load(img_dir)
                    feature_data = np.load(feature_dir)
                
                except Exception as e:
                    #np.savez(img_dir, *self.dataList)
                    np.savez(feature_dir, *self.features)
                    print(str(e))
                    print("Created new file -> ", feature_dir)
                    self.destroy()
                    return

                
                
                old_imgs = []
                old_features = []

                # Move into a usable array
                for key in img_data:
                    old_imgs.append((img_data[key]))

                    
                for key in feature_data:
                    old_features.append((feature_data[key]))

                # Add new data to array
                #for new_img in self.dataList:
                #    old_imgs.append(new_img)

                    
                # Add new data to array
                for new_feature in self.features:
                    old_features.append(new_feature)



                # Save new data
                np.savez(img_dir, *old_imgs)
                np.savez(feature_dir, *old_features)
                
                self.destroy()
                return



            # Clear after each letter submission
            self.clear()

