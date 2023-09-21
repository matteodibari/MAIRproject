import keras
import numpy as np
import collections
from sklearn import model_selection

words = None

def sentence_to_vector(sentence):
    array = np.zeros(29)
    if 'bye' in sentence:
        array[0] = 1
    if 'goodbye' in sentence:
        array[1] = 1
    if 'yes' in sentence:
        array[2] = 1
    if 'right' in sentence:
        array[3] = 1
    if 'confirm' in sentence:
        array[4] = 1
    if 'no ' in sentence:
        array[5] = 1
    if sentence == 'not':
        array[6] = 1
    if 'hi ' in sentence:
        array[7] = 1
    if 'hello' in sentence:
        array[8] = 1
    if 'more' in sentence:
        array[9] = 1
    if 'how about' in sentence:
        array[10] = 1
    if 'anything else' in sentence:
        array[11] = 1
    if 'start over' in sentence:
        array[12] = 1
    if 'repeat' in sentence:
        array[13] = 1
    if 'reset' in sentence:
        array[14] = 1
    if 'thank' in sentence:
        array[15] = 1
    if 'dont want' in sentence:
        array[16] = 1
    if 'wrong' in sentence:
        array[17] = 1
    if sentence == 'cough':
        array[18] = 1
    if sentence == 'unintelligible':
        array[19] = 1
    if sentence == 'sil':
        array[20] = 1
    if 'is it ' in sentence:
        array[21] = 1
    if 'does it ' in sentence:
        array[22] = 1
    if 'what' in sentence:
        array[23] = 1
    if 'which' in sentence:
        array[24] = 1
    if 'when' in sentence:
        array[25] = 1
    if 'phone' in sentence:
        array[26] = 1
    if 'address' in sentence:
        array[27] = 1
    if 'price' in sentence:
        array[28] = 1
    return array

def label_to_vector(label):
    array = np.zeros(15)
    match label:
        case 'ack':
            array[0] = 1
        case 'affirm':
            array[1] = 1
        case 'bye':
            array[2] = 1
        case 'confirm':
            array[3] = 1
        case 'deny':
            array[4] = 1
        case 'hello':
            array[5] = 1
        case 'inform':
            array[6] = 1
        case 'negate':
            array[7] = 1
        case 'null':
            array[8] = 1
        case 'repeat':
            array[9] = 1
        case 'reqalts':
            array[10] = 1
        case 'reqmore':
            array[11] = 1
        case 'request':
            array[12] = 1
        case 'restart':
            array[13] = 1
        case 'thankyou':
            array[14] = 1
    return array

def vector_to_label(array):
    if array[0]:
        label = 'ack'
    if array[1]:
        label = 'affirm'
    if array[2]:
        label = 'bye'
    if array[3]:
        label = 'confirm'
    if array[4]:
        label = 'deny'
    if array[5]:
        label = 'hello'
    if array[6]:
        label = 'inform'
    if array[7]:
        label = 'negate'
    if array[8]:
        label = 'null'
    if array[9]:
        label = 'repeat'
    if array[10]:
        label = 'reqalts'
    if array[11]:
        label = 'reqmore'
    if array[12]:
        label = 'request'
    if array[13]:
        label = 'restart'
    if array[14]:
        label = 'thankyou'
    return label

def bag_of_words(data):
    # Use once, returns an array with all words used by the model
    # data = np.array(data, dtype='O')
    data = [string.split() for string in data]
    data = [word for sent in data for word in sent]
    
    bagofwords = collections.Counter(data)
    bagofwords = {word:count for word, count in bagofwords.items() if count >= 2}
    return list(bagofwords.keys())

def sentence_to_vector_2(sentence, words):
    # generate list of words:
    array = np.zeros(len(words))
    for word in sentence:
        # check if 
        if word in words:
            array[words.index(word)] = 1
    return array

def get_data():
    datContent = [i.strip().split(' ', 1) for i in open("./dialog_acts.dat").readlines()]
    np.random.shuffle(datContent)
    array = np.array(datContent)
    x_train, x_test, y_train, y_test = model_selection.train_test_split(array[:,1], array[:,0], test_size=0.15, random_state=42)
    return x_train, x_test, y_train, y_test

def train_model():
    global words

    x_train, x_test, y_train, y_test = get_data()
    words = bag_of_words(x_train)

    x_train_vectors = list()
    for i in range(len(x_train)):
        x_train_vectors.append(sentence_to_vector_2(x_train[i], words))
    x_train_vectors = np.array(x_train_vectors)

    y_train_vectors = list()
    for i in range(len(y_train)):
        y_train_vectors.append(label_to_vector(y_train[i]))
    y_train_vectors = np.array(y_train_vectors)

    model = keras.Sequential()
    model.add(keras.layers.Dense(256, input_shape=(len(words),)))
    model.add(keras.layers.Dense(512, activation='relu'))
    model.add(keras.layers.Dense(15, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adam(), metrics='accuracy')

    history = model.fit(x_train_vectors, y_train_vectors, batch_size=128, epochs=22, verbose=1, validation_split=0.2)
    
    x_test_vectors = list()
    for i in range(len(x_test)):
        x_test_vectors.append(sentence_to_vector_2(x_test[i], words))
    x_test_vectors = np.array(x_test_vectors)

    y_test_vectors_pred = model(x_test_vectors)

    y_test_pred = list()
    for i in range(len(y_test_vectors_pred)):
        y_test_pred.append(vector_to_label(y_test_vectors_pred[i]))
    y_test_pred = np.array(y_test_pred)

    y_test_vectors = list()
    for i in range(len(y_test)):
        y_test_vectors.append(label_to_vector(y_test[i]))
    y_test_vectors = np.array(y_test_vectors)

    print(model.evaluate(x_test_vectors, y_test_vectors))

    model.save('saved_model.h5', overwrite=True)

    