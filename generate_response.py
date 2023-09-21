import numpy as np
from keras.models import load_model
from model_feed_forward import sentence_to_vector_2
from model_feed_forward import vector_to_label

def generate_response(input_msg):
    #define the states
    curr_state = 1
    #categorize the input sentence
    model = load_model('saved_model.h5')

    #read the bag of words from the file
    words = None
    with open('bag_of_words.txt', 'r') as f:
        data = f.read()
        words = data.split('\n')

    y = model.predict( np.array( [sentence_to_vector_2(input_msg, words),] ))
    print(vector_to_label(y[0]))

generate_response('what')
