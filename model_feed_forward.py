import keras
import numpy as np
import collections
from sklearn import model_selection
from keras import backend as K

words = None

def to_one_hot(array):
    """
    This function takes an array and returns its "one-hot" version
    using the position of its highest element.

    :param array: sentence to use for the prediction.
    :return result: resulting one-hot array.
    """

    max_index = list(array).index(max(array))
    result = np.zeros(len(array))
    result[max_index] = 1
    return result

def label_to_vector(label):
    """
    This function returns the vectorised version of a label.

    :param label: label to vectorize.
    :return array: resulting vector.
    """

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
    """
    This function, given a one-hot array, returns its respective label.

    :param array: one-hot array.
    :return label: resulting label.
    """

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
    """
    This function takes an array of strings and return a list containing the words
    that show up at least 2 times in total.

    :param data: array of strings.
    :return: bag of words.
    """

    data = [string.split() for string in data]
    data = [word for sent in data for word in sent]
    
    bagofwords = collections.Counter(data)
    bagofwords = {word:count for word, count in bagofwords.items() if count >= 2}
    return list(bagofwords.keys())

def sentence_to_vector_2(sentence, bag_of_words):
    """
    This function vectorizes a sentence using a bag of words.

    :param sentence: sentence to vectorize.
    :param bag_of_words: bag of words to use for the vectorization.
    :return array: resulting vectorized version. .
    """

    array = np.zeros(len(bag_of_words))
    for word in sentence:
        if word in bag_of_words:
            array[bag_of_words.index(word)] = 1
    return array

def get_data(without_duplicates=False):
    """
    This function takes all the given data, shuffles it, and divides it in 2 parts:
    the first 85% for the training set and the remaining 15% for the test set.

    :return (x_train, y_train, x_test, y_train): Returns respectively the training input,
    the training output, the test input and the test output. 
    """

    if without_duplicates:
        datContent = [i.strip().split(' ', 1) for i in open("./dialog_acts_deduplicated.dat").readlines()]    
    else:
        datContent = [i.strip().split(' ', 1) for i in open("./dialog_acts.dat").readlines()]
    
    np.random.shuffle(datContent)
    array = np.array(datContent)
    x_train, x_test, y_train, y_test = model_selection.train_test_split(array[:,1], array[:,0], test_size=0.15, random_state=42)
    return x_train, x_test, y_train, y_test

def recall_m(y_true, y_pred):
    """
    Function to compute recall.

    :param y_true: true labels.
    :param y_pred: predicted labels.
    :return recall: computed recall.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    """
    Function to compute precision.

    :param y_true: true labels.
    :param y_pred: predicted labels.
    :return precision: computed precision.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def train_model(without_duplicates=False):
    """
    This function uses the data and the bag of words to train and subsequently test 
    a keras model.
    """
    global words

    x_train, x_test, y_train, y_test = get_data(without_duplicates)
    words = bag_of_words(x_train)

    # with open('bag_of_words.txt', 'w') as f:
    #     for word in words:
    #         f.write(str(word) + '\n')

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
    model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adam(), metrics=['acc',precision_m, recall_m])

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
    # model.save('saved_model.h5', overwrite=True)

    # y = model.predict( np.array( [sentence_to_vector_2('goodbye', words)] ))
    # y = to_one_hot(y[0])
    # print(y)
    # print(vector_to_label(y))

