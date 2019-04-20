import numpy as np  
import matplotlib.pyplot as plt
from string import ascii_lowercase
np.random.seed(420)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})


        
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


plz = []
ans = []


for i in data:
    for j in range(len(i)-2):
        #print(j)
        plz.append(i[j])



training_outputs = np.array(labels)

inputs = np.array(plz)


training_outputs = np.array(labels)

feature_set = np.vstack(np.divide(inputs,4080))


one_hot_labels = np.zeros((len(labels), 26))



for i in range(len(labels)):  
    one_hot_labels[i, labels[i]] = 1




loaded = False

try:
    h = np.load("./wh.npz")
    hb = np.load("./bh.npz")
    o = np.load("./wo.npz")
    ob = np.load("./bo.npz")
    loaded = True

except Exception as e:
    print(str(e))




def sigmoid(x):  
    return 1/(1+np.exp(-x))

def sigmoid_der(x):  
    return sigmoid(x) *(1-sigmoid (x))

def softmax(A, axel = 1):  
    expA = np.exp(A)
    return expA / expA.sum(axis=axel, keepdims=True)

if(not loaded):


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

    for epoch in range(100000):  
    ############# feedforward

        # Phase 1
        zh = np.dot(feature_set, wh) + bh
        ah = sigmoid(zh)

        # Phase 2
        zo = np.dot(ah, wo) + bo
        ao = softmax(zo)



    ########## Back Propagation

    ########## Phase 1

        dcost_dzo = ao - one_hot_labels
        dzo_dwo = ah

        dcost_wo = np.dot(dzo_dwo.T, dcost_dzo)

        dcost_bo = dcost_dzo

    ########## Phases 2

        dzo_dah = wo
        dcost_dah = np.dot(dcost_dzo , dzo_dah.T)
        dah_dzh = sigmoid_der(zh)
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
            #print('Loss function value: ', loss)
            error_cost.append(loss)
            print("loss: " , loss)


else:

    one = "one"
    wh = h[one]
    bh = hb[one]
    wo = o[one]
    bo = ob[one]
    


def think(feature):
    # Phase 1
    zh = np.dot(feature, wh) + bh
    ah = sigmoid(zh)

    # Phase 2
    zo = np.dot(ah, wo) + bo
    ao = softmax(zo,0)

    print(ao)
    return np.argmax(ao)



np.savez("./wh.npz", one = wh)
np.savez("./bh.npz", one = bh)
np.savez("./wo.npz", one = wo)
np.savez("./bo.npz", one = bo)



correct = 0
i = 0


for letter in ascii_lowercase:

    prediction = ascii_lowercase[think(np.divide(test_data[i],4080))]
    print("(" + letter + ") ", "I think it's an: ", prediction)

    if(prediction == letter):
        correct += 1

    i+=1


print("I got ", correct, " letters right out of 26")
print(correct, '/', 26, '=', correct/26)



