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
        self.net.load()

        #for K nearest Neighbors
        self.data = []
        self.test_data = []
        self.knn = KNeighborsClassifier()
        self.load_knn()

        
    def saveq(self):
        
        self.save("user_input/" + self.filename)
        self.display()


    def load_knn(self):


        self.loadee()
        labels = [0]*416
        counter = 0
        let = 0
        for i in range(len(labels)):
            labels[i] = let
            counter += 1

            if(not(counter%16)):
                let += 1

        plz = []
        test = []
        count = 0
        for i in self.data:
            for j in range(len(i)-2):
                #print(j)
                plz.append(i[j])

            test.append(self.test_data[count])
            
            count +=1


        self.knn.fit(plz, labels)
        KNeighborsClassifier(algorithm='auto', 
                     leaf_size=30, 
                     metric='minkowski',
                     metric_params=None, 
                     n_jobs=1, 
                     n_neighbors=5, 
                     p=2,
                     weights='uniform')
        
        #print("Predictions form the classifier:")
        #print(self.knn.predict(test))
        #print("Target values:")
        #rint([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])


        
    def loader(self, letter):

        print("loader!")
        l = []
        for key in letter:
            l.append(letter[key])

        #print(len(l))
        self.data.append(l)
        #print("loading => ", l[16])
        self.test_data.append(l[16])
        #print("test_data: ", self.test_data)

    def loadee(self):
        
        for i in ascii_lowercase:
            print("loading: ", i)
            letter = np.load("./data/features/" + i + ".npz")
            self.loader(letter)
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
        #boundingBoxes = [cv2.boundingRect(c) for c in contours]
        #(cnts, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes),
        #key=lambda b:b[1][i], reverse=reverse))

        
        for i in range(len(contours)):
            
            x,y,w,h = cv2.boundingRect(contours[i])
     
            #cv2.rectangle(copy,         # Draw rectangle on temporary copy
             #            (x, y),        # Start
              #           (x+w,y+h),     # End
               #          (255, 0, 0),   # BGR value (RGB backwards)
                #          2)            # Thickness

            imgROI = image[y:y+h, x:x+w]

            #cv2.imshow("hello", imgROI)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            unsorted_list.append([x + (y+h)*5,self.get_feature(imgROI),contours[i]])

            #self.net.print(self.get_feature(imgROI))


        
        unsorted_list.sort(key = lambda x: x[0])



        
            


        for i in unsorted_list:
            print(i[0])
            self.net.print(i[1])
            print("knn thinkgs it's a: ", ascii_lowercase[int(self.knn.predict([i[1]])[0])])
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
            
            
            
        #self.destroy()
        cv2.imshow("user_input", copy)
        cv2.waitKey(0)
