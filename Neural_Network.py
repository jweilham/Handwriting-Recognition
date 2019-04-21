import numpy as np  
import matplotlib.pyplot as plt
from string import ascii_lowercase

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

class Neural_Network():
    
    def __init__(self):
        # seeding for random number generation
        np.random.seed(420)

        self.wh = None
        self.bh = None
        
        self.wo = None
        self.bo = None
        self.loaded = False
        
        self.outputs = ascii_lowercase
        
        
    def one_hot(self, labels):

        one_hot_labels = np.zeros((len(labels), 26))
        
        for i in range(len(labels)):  
            one_hot_labels[i, labels[i]] = 1
            print(one_hot_labels[i])

    
        return one_hot_labels


        
    def load(self):
	
        try:
                h = np.load("./wh.npz")
                hb = np.load("./bh.npz")
                o = np.load("./wo.npz")
                ob = np.load("./bo.npz")
                self.loaded = True
                
                one = "one"
                self.wh = h[one]
                self.bh = hb[one]
                self.wo = o[one]
                self.bo = ob[one]
                
                

        except Exception as e:
                print(str(e))
                

    def sigmoid(self, x):  
        return 1/(1+np.exp(-x))

    def sigmoid_der(self, x):  
        return self.sigmoid(x) *(1-self.sigmoid (x))

    def softmax(self, A, axel = 1):  
        expA = np.exp(A)
        return expA / expA.sum(axis=axel, keepdims=True)


    def train(self, feature_array, labels, iterations):

        feature_set = np.vstack(feature_array)

        # How many features do we have
        instances = feature_set.shape[0]

        # Size of each feature (dimensionss)
        attributes = feature_set.shape[1]

        print("instances", instances)
        print("attributes", attributes)
        
        one_hot_labels = self.one_hot(labels)


        hidden_nodes = 50  
        output_labels = 26


        # Weights to hidden nodes/Bias of nodes
        self.wh = np.random.rand(attributes,hidden_nodes)
        self.bh = np.random.randn(hidden_nodes)

        # Weights to the output nodes/Bias of nodes
        self.wo = np.random.rand(hidden_nodes,output_labels)
        self.bo = np.random.randn(output_labels)

        
        # Learning rate
        lr = 0.005

        error_cost = []

        for epoch in range(10000):  
        ############# feedforward

            # Phase 1
            zh = np.dot(feature_set, self.wh) + self.bh
            ah = self.sigmoid(zh)

            # Phase 2
            zo = np.dot(ah, self.wo) + self.bo
            ao = self.softmax(zo)



        ########## Back Propagation

        ########## Phase 1

            dcost_dzo = ao - one_hot_labels
            dzo_dwo = ah

            dcost_wo = np.dot(dzo_dwo.T, dcost_dzo)

            dcost_bo = dcost_dzo

        ########## Phases 2

            dzo_dah = self.wo
            dcost_dah = np.dot(dcost_dzo , dzo_dah.T)
            dah_dzh = self.sigmoid_der(zh)
            dzh_dwh = feature_set
            dcost_wh = np.dot(dzh_dwh.T, dah_dzh * dcost_dah)

            dcost_bh = dcost_dah * dah_dzh

            # Update Weights ================

            self.wh -= lr * dcost_wh
            self.bh -= lr * dcost_bh.sum(axis=0)

            self.wo -= lr * dcost_wo
            self.bo -= lr * dcost_bo.sum(axis=0)

            if epoch % 200 == 0:
                loss = np.sum(-one_hot_labels * np.log(ao))
                #print('Loss function value: ', loss)
                error_cost.append(loss)
                print("loss: " , loss)

				
    # returns output number it thinks it is		
    def think(self, feature):
        # Phase 1
        zh = np.dot(feature, self.wh) + self.bh
        ah = self.sigmoid(zh)

        # Phase 2
        zo = np.dot(ah, self.wo) + self.bo
        ao = self.softmax(zo,0)

        print(ao)
        return np.argmax(ao)


    def print(self, feature):
    
        prediction = self.outputs[self.think(feature)]
        print("I think it's an: ", prediction)




data = []
test_data = []


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



loadee()


labels = [0]*416
counter = 0
let = 0
for i in range(len(labels)):
    labels[i] = let
    counter += 1

    if(not(counter%16)):
        let += 1


print(labels)

plz = []
ans = []


for i in data:
    for j in range(len(i)-2):
        #print(j)
        plz.append(i[j])



training_outputs = np.array(labels)

inputs = np.array(plz)


n = Neural_Network()

n.train(inputs, training_outputs, 50000)

n.print(test_data[0])


one_hot_labels = np.zeros((len(labels), 26))




