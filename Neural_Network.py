import numpy as np  
import matplotlib.pyplot as plt
from string import ascii_lowercase

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

# Most of neural net implementation obtained from
# https://stackabuse.com/creating-a-neural-network-from-scratch-in-python-multi-class-classification/


class Neural_Network():
    
    def __init__(self):

        np.random.seed(200)

        # Weights and bias of hidden layer nodes
        self.wh = None
        self.bh = None
        
        # Weights and bias of output layer nodes
        self.wo = None
        self.bo = None

        # For saving net state
        self.loaded = False

        self.outputs = ascii_lowercase
        
    
    def one_hot(self, labels):

        one_hot_labels = np.zeros((len(labels), 26))
        
        for i in range(len(labels)):  
            one_hot_labels[i, labels[i]] = 1
    
        return one_hot_labels


    # Save weights for NN
    def save(self):

        np.savez("./data/network/wh.npz", one = self.wh)
        np.savez("./data/network/bh.npz", one = self.bh)
        np.savez("./data/network/wo.npz", one = self.wo)
        np.savez("./data/network/bo.npz", one = self.bo)
    
    # Load weights
    def load(self):
	
        try:
                h = np.load("./data/network/wh.npz")
                hb = np.load("./data/network/bh.npz")
                o = np.load("./data/network/wo.npz")
                ob = np.load("./data/network/bo.npz")
                
                
                one = "one"
                self.wh = h[one]
                self.bh = hb[one]
                self.wo = o[one]
                self.bo = ob[one]
                self.loaded = True
                

        except Exception as e:
                print(str(e))
                
    # Used to normalize weights at each layer
    def sigmoid(self, x):  
        return 1/(1+np.exp(-x))

    def sigmoid_der(self, x):  
        return self.sigmoid(x) *(1-self.sigmoid (x))

    # Returns array of percentages for which letter the NN thinks the input is
    def softmax(self, A, axel = 1):  
        expA = np.exp(A)
        return expA / expA.sum(axis=axel, keepdims=True)

    # Updates weights based on feature array as input
    def train(self, feature_array, labels, iterations):

        feature_set = np.vstack(feature_array)

        one_hot_labels = self.one_hot(labels)
        instances = feature_set.shape[0]

        attributes = feature_set.shape[1]

        hidden_nodes = 50  
        output_labels = 26

        # Weights to hidden nodes/Bias of nodes
        wh = np.random.rand(attributes,hidden_nodes)
        bh = np.random.randn(hidden_nodes)

        # Weights to the output nodes/Bias of nodes
        wo = np.random.rand(hidden_nodes,output_labels)
        bo = np.random.randn(output_labels)

        # Learning rate
        lr = 0.005

        error_cost = []

        for epoch in range(iterations):  
            ############# feedforward

            # Phase 1
            zh = np.dot(feature_set, wh) + bh
            ah = self.sigmoid(zh)

            # Phase 2
            zo = np.dot(ah, wo) + bo
            ao = self.softmax(zo)

            ########## Back Propagation

            ########## Phase 1

            dcost_dzo = ao - one_hot_labels
            dzo_dwo = ah

            dcost_wo = np.dot(dzo_dwo.T, dcost_dzo)

            dcost_bo = dcost_dzo

            ########## Phases 2

            dzo_dah = wo
            dcost_dah = np.dot(dcost_dzo , dzo_dah.T)
            dah_dzh = self.sigmoid_der(zh)
            dzh_dwh = feature_set
            dcost_wh = np.dot(dzh_dwh.T, dah_dzh * dcost_dah)

            dcost_bh = dcost_dah * dah_dzh

            # Update Weights ================

            wh -= lr * dcost_wh
            bh -= lr * dcost_bh.sum(axis=0)

            wo -= lr * dcost_wo
            bo -= lr * dcost_bo.sum(axis=0)

            if epoch % 200 == 0:
                loss = np.sum(-one_hot_labels * np.log(ao))
                print('Loss function value: ', loss)
                error_cost.append(loss)
                print("loss: " , loss)

        self.bh = bh
        self.wh = wh
        self.wo = wo
        self.bo = bo

				
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
