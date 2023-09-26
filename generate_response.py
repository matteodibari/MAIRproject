import numpy as np
from keras.models import load_model
from model_feed_forward import sentence_to_vector_2
from model_feed_forward import vector_to_label


curr_state = 1

#stored-data = [area, type, price-range]
stored_data = [None, None, None]

apologies = ['Sorry, I did not find any restaurant matching these preferences.']
ask_area = ['In which area are you searching for the restaurant?']
ask_type = ['Which type of food are you searching for?']
bye = ['Bye man!']
error = ['Sorry, I did not understand what you meant.']

model = load_model('saved_model.h5')
words = None
with open('bag_of_words.txt', 'r') as f:
    data = f.read()
    words = data.split('\n')

y = model.predict( np.array( [sentence_to_vector_2(input_msg, words),] ))
print(vector_to_label(y[0]))


print('Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?')

while(1):
    user_input = input()
    dialog_act = 'thankyou'

    #get informations from the input

    match curr_state:
        case 1:
            if stored_data[0] == None: 
                print(ask_area[0])
                curr_state = 2
            elif stored_data[1] == None:
                print(ask_type[0])
                curr_state = 3
            else:
                #search for a restaurant
                if 'found':
                    curr_state = 4
                    #give suggestion
                else:
                    curr_state = 5
                    print(apologies[0])
        case 2:
            if 'none':
                curr_state = 2
                continue

            if stored_data[1] == None:
                print(ask_type[0])
                curr_state = 3
            else:
                #search for a restaurant
                if 'found':
                    curr_state = 4
                    #give suggestion
                else:
                    curr_state = 5
                    print(apologies[0])

        case 3:
            if 'none':
                curr_state = 3
                continue
            
            #search for a restaurant
            if 'found':
                curr_state = 4
                #give suggestion
            else:
                curr_state = 5
                print(apologies[0])

        case 4:
            if dialog_act == 'reqalts':
                #search for a restaurant
                if 'found':
                    curr_state = 4
                    #give suggestion
                else:
                    curr_state = 5
                    print(apologies[0])
            elif dialog_act in ['request', 'reqmore']:
                # search for the infos
                # give the info
                curr_state = 7
            elif dialog_act == 'thankyou':
                print(bye[0])
                exit()
            else:
                if dialog_act == 'repeat':
                    continue
                else:
                    print(error[0])          
        case 5:
            if stored_data[0] == None: 
                curr_state = 2
            elif stored_data[1] == None:
                curr_state = 3
            else:
                #search for a restaurant
                if 'found':
                    curr_state = 4
                    #give suggestion
                else:
                    curr_state = 5
                    #apologize




def generate_response(input_msg, curr_state):
    #define the states

    #categorize the input sentence
    # model = load_model('saved_model.h5')

    #read the bag of words from the file
    # words = None
    # with open('bag_of_words.txt', 'r') as f:
    #     data = f.read()
    #     words = data.split('\n')

    # y = model.predict( np.array( [sentence_to_vector_2(input_msg, words),] ))
    # print(vector_to_label(y[0]))
    pass
  
generate_response('what')
