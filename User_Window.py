from Window import *
import time
from Neural_Network import*
from sklearn.neighbors import KNeighborsClassifier
from string import ascii_lowercase

class User_Window(Window):


    def __init__(self):
        Window.__init__(self, w = 700, h = 500)
        
	    # Update menubar
        self.menubar.insert_command(0, label = "Save & Quit", command=self.saveq)
        self.menubar.insert_command(0, label = "Use last input", command=self.last)
        self.config(menu=self.menubar)
        
        self.net = Neural_Network()
        #self.net.load() # used if you want to use saved neural net state

        #for K nearest Neighbors
        self.data = []
        self.test_data = []
        self.knn = KNeighborsClassifier()
        self.load_knn()

        
    def saveq(self):
        
        self.save("user_input/" + self.filename)
        self.display()


    def load_knn(self):


        self.load_data()
        print("DATA LENGTH: ", len(self.data))
        # Makes labels array, 
        labels = [0]*(len(self.data))*(len(self.data[0]))
        counter = 0
        let = 0
        training_data = []

        for i in range(len(labels)):
            labels[i] = let
            counter += 1

            #print("COUNTER ", counter, " LENGTH of data[counter] ", len(self.data[counter]))
            #print("logic: ", counter%(len(self.data[counter])))
            if(not(counter%(len(self.data[counter])))):
                counter = 0
                let += 1

        print(labels)

        testing_data = []
        count = 0
        for i in self.data:
            for j in range(len(i)):
                training_data.append(i[j])
            
            count +=1

        self.net.train(training_data, labels, 1500)
        self.net.save()
    
    def load_letter(self, letter):

        l = []
        for key in letter:
            l.append(letter[key])
            
        self.data.append(l)

    def load_data(self):
        
        for i in ascii_lowercase:
            print("loading: ", i)
            letter = np.load("./data/features/" + i + ".npz")
            self.load_letter(letter)

    def last(self):
        
        self.display()

    def display(self):
        
        # Reads in our image as a numpy array
        image = cv2.imread("user_input/" + self.filename + ".TIFF")
        
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

        cv2.imshow("dialated", dilated)
        cv2.waitKey(0)
    
        
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        for c in contours:
            hull = cv2.convexHull(c)
            print(type(hull))
            print(type([hull]))
            cv2.drawContours(copy, [hull], -1, (0, 0, 255), 1)

        cv2.imshow('convex hull', copy)
        cv2.waitKey(0)

        start = time.time()
        
        letter_detection.beautify(contours, copy)
        print("--- %s seconds ---" % (time.time() - start))

        unsorted_list = []
        features = []

        i = 1
        reverse = False
        
        for i in range(len(contours)):
            
            x,y,w,h = cv2.boundingRect(contours[i])

            imgROI = image[y:y+h, x:x+w]

            # Give height and x value weights to try and sort them Left to Right, Top to Bottom
            unsorted_list.append([x + (y+h)*5,self.get_feature(imgROI),contours[i]])

        unsorted_list.sort(key = lambda x: x[0])

        # neural net output
        print("neural net output")
        for i in unsorted_list:
            print(ascii_lowercase[self.net.think(i[1])])
            x,y,w,h = cv2.boundingRect(i[2])
     
            cv2.rectangle(copy,         # Draw rectangle on temporary copy
                         (x, y),        # Start
                         (x+w,y+h),     # End
                         (255, 0, 0),   # BGR value (RGB backwards)
                          2)            # Thickness

            imgROI = image[y:y+h, x:x+w]

            cv2.imshow("hello", imgROI)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        for i in unsorted_list:
            
            x,y,w,h = cv2.boundingRect(i[2])
     
            cv2.rectangle(copy,         # Draw rectangle on temporary copy
                         (x, y),        # Start
                         (x+w,y+h),     # End
                         (255, 0, 0),   # BGR value (RGB backwards)
                          2)            # Thickness

            imgROI = image[y:y+h, x:x+w]

            cv2.imshow("hello", imgROI)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        cv2.imshow("user_input", copy)
        cv2.waitKey(0)
