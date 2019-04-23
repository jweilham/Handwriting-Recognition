from Window import Window   # window class for user input
import cv2                  # opencv for reading data from images
import numpy as np          # use of multidimensional numpy arrays
import time                 # determine how efficient program is
import letter_detection     # detecting i's and j's
from Letter_Window import *
from User_Window import *
from string import ascii_lowercase
# Create and fit a nearest-neighbor classifier
from sklearn.neighbors import KNeighborsClassifier

data = []
test_data = []

def alphabet():

    for i in ascii_lowercase:
        data = []
        load = np.load("./data/features/" + i + ".npz")

        j = 0
        for key in load:
            data.append(load[key])
            #print(i, data[j])
            j+=1



def loader(letter):
    l = []
    for key in letter:
        l.append(letter[key])

    #print(len(l))
    data.append(l)
    test_data.append(l[16])

def loadee():
    
    for i in ascii_lowercase:
        print("loading: ", i)
        letter = np.load("./data/features/" + i + ".npz")
        loader(letter)

def main():

    labels = [0]*416
    counter = 0
    let = 0
    for i in range(len(labels)):
        labels[i] = let
        counter += 1

        if(not(counter%16)):
            let += 1

    loadee()

    plz = []
    test = []
    count = 0
    for i in data:
        for j in range(len(i)-2):
            #print(j)
            plz.append(i[j])

        test.append(test_data[count])
        count +=1

    print(labels)
        
    knn = KNeighborsClassifier()
    knn.fit(plz, labels) 
    KNeighborsClassifier(algorithm='auto', 
                         leaf_size=30, 
                         metric='minkowski',
                         metric_params=None, 
                         n_jobs=1, 
                         n_neighbors=5, 
                         p=2,
                         weights='uniform')
    print("Predictions form the classifier:")
    print(knn.predict(test))
    print("Target values:")
    print([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])

    #alphabet()

    y = User_Window()
    y.mainloop()


    for i in ascii_lowercase:
        print(i)
        #data = Letter_Window(i)
        #data.mainloop()
        
if __name__ == "__main__":
    main()


