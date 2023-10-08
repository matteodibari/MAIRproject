import numpy as np
from keras.models import load_model

from model_feed_forward import sentence_to_vector_2
from model_feed_forward import vector_to_label
from model_feed_forward import to_one_hot

from user_pref import get_user_pref
from user_pref import recommend
from user_pref import get_user_request
from user_pref import check_dont_care

from text_speech import text_to_speech
from text_speech import speech_to_text

# Uncomment these 2 lines if you get this warning:
# I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
# To enable the following instructions: SSE SSE2 SSE3 SSE4.1 SSE4.2 AVX AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
#
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

curr_state = 1

input_type = None
#this variable is set in the first iteration of the loop. It will be 1 if the input is from keyboard, 2 if the input is from microphone

stored_preferences = [None, None, None]
#stored-preferences = [price-range, area, type]

ask_area = ['In which area are you searching for the restaurant?']
ask_type = ['Which type of food are you searching for?']
bye = ['Goodbye!']
error = ['Sorry, I did not understand what you meant.']

random_output = 'no'
levenshtein_precision = 5

def add_customisations():
    """
    This function takes user input and modifies parameters for the Levenshtein edit distance
    and the order in which restaurants are chosen.
    """
    global random_output
    global levenshtein_precision
    customiseInput = input("Do you want to add customizations to the system? (yes/no)\n")
    if customiseInput == 'yes':
        random_output = input("Do you want the suggestions to be given in random order? (yes/no)\n")
        distancePrecision = input("What degree of precision would you like for the Levenshtein disance? (low/medium/high)\n")
        if distancePrecision == 'low':
            levenshtein_precision = 2
        if distancePrecision == 'high':
            levenshtein_precision = 7

def get_user_input():
    """
    This function helps the user choose the way they input the message and gets the input as return
    """
    global input_type

    if input_type == None:
        print('Set the way you want to input the messages. (Type 1 for keyboard input, 2 for voice input)')
        input_type = input()
        return

    if int(input_type) == 1:
        message = input()
    else:
        message = speech_to_text()
    return message


def print_aditional_info(aditional_info):
    """
    This function prints information about the best restaurant in a user-friendly manner.

    :param additional_info: info to be printed.
    """

    if aditional_info[10] is not None:

        type = ''
        explanation = ''
        if aditional_info[10] == 'touristic':
            type = 'is good for tourists'
            if aditional_info[1] == 'cheap':
                explanation = ' the restaurant is cheap.'
            elif aditional_info[7] == 'good':
                explanation = 'the food is good.'
            else:
                explanation = 'it is cheap and the food is good.'
        if aditional_info[10] == 'assignedseats':
            type = 'seats are assigned by the restaurant'
            explanation = 'it is quite a busy place.'
        if aditional_info[10] == 'children':
            type = 'is good for children'
            explanation = 'it does not allow you to stay for a long time.'
        if aditional_info[10] == 'romantic':
            type = 'is romantic'
            explanation = 'it allows you to stay for a long time.'
        print('The restaurant ' + type + ', because ' + explanation)
        text_to_speech('The restaurant ' + type + ', because ' + explanation)


def print_restaurant(restaurant_info):
    """
    This function prints the suggestion given the information of a restaurant.

    :param restaurant_info: information of the restaurant.
    """

    if len(restaurant_info) == 1:
        print('Sorry, there is no restaurant with these requirements.')
        text_to_speech('Sorry, there is no restaurant with these requirements.')
        return

    print('The perfect restaurant is ' + restaurant_info[0] + ' with ' + restaurant_info[1] +
                          ' price range which is located in ' + restaurant_info [2] + ' part of the town and serves '
                          + restaurant_info[3] + ' food.')
    info = str('The perfect restaurant is ' + restaurant_info[0] + ' with ' + restaurant_info[1] +
                          ' price range which is located in ' + restaurant_info [2] + ' part of the town and serves '
                          + restaurant_info[3] + ' food.')
    text_to_speech(info)
    print_aditional_info(restaurant_info)

    return

def print_apologies():
    """
    This function prints the apologies given the current user preferences.
    """

    print(f'Sorry, I did not find any restaurant matching these preferences: {stored_preferences[0]}, {stored_preferences[1]}, {stored_preferences[2]}. Please search again.')
    text_to_speech(f'Sorry, I did not find any restaurant matching these preferences: {stored_preferences[0]}, {stored_preferences[1]}, {stored_preferences[2]}. Please search again.')

def predict_dialog_act(input_msg):
    """
    This function uses a pretrained model to predict the dialog act
    given a sentence.

    :param input_msg: sentence to use for the prediction.
    """

    model = load_model('saved_model.h5')
    words = None
    with open('bag_of_words.txt', 'r') as f:
        data = f.read()
        words = data.split('\n')

    y = model.predict( np.array( [sentence_to_vector_2(input_msg, words),] ), verbose=0)
    y = to_one_hot(y[0])
    return vector_to_label(y)

already_recommended = []

add_customisations()
get_user_input() #this function call is used to set the type of input (keyboard or microphone)
print('Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?')
text_to_speech('Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?')

while(1):
    '''
    This is the main process of the system, consisting in the state transitioning function. Its main component
    is a python switch that based on the curr_state variable performs the relative actions (as modelled in the 
    state diagram).
    '''
    user_input = get_user_input()
    dialog_act = predict_dialog_act(user_input)
    print(dialog_act)

    if dialog_act == 'restart':
        print('System restarting...')
        text_to_speech('System restarting...')
        stored_preferences = [None, None, None]
        already_recommended = []
        print('Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?')
        text_to_speech('Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?')
        curr_state = 1
        continue

    preferences_changed = False

    #clearing the preferences if we entered in state 5
    if curr_state == 5:
        stored_preferences = [None, None, None]

    preferences = get_user_pref(user_input, levenshtein_precision)
    # preferences[3] = [price, location, typeoffood]

    for i in range(len(stored_preferences)):
        if preferences[i] != None:
            stored_preferences[i] = preferences[i]
            preferences_changed = True

    match curr_state:
        case 1:

            if stored_preferences[1] == None:
                print(ask_area[0])
                text_to_speech(ask_area[0])
                curr_state = 2
            elif stored_preferences[2] == None:
                print(ask_type[0])
                text_to_speech(ask_type[0])
                curr_state = 3
            else:
                restaurant_info = recommend(stored_preferences, already_recommended, random_output)

                if restaurant_info:
                    already_recommended.append(restaurant_info)
                    curr_state = 4
                    print_restaurant(restaurant_info)
                else:
                    curr_state = 5
                    print_apologies()
        case 2:

            if check_dont_care(user_input, levenshtein_precision):
                stored_preferences[1] = 'any'

            if dialog_act == 'None':
                curr_state = 2
                continue

            if stored_preferences[2] == None:
                print(ask_type[0])
                text_to_speech(ask_type[0])
                curr_state = 3
            else:
                restaurant_info = recommend(stored_preferences, already_recommended, random_output)

                if restaurant_info:
                    already_recommended.append(restaurant_info)
                    curr_state = 4
                    print_restaurant(restaurant_info)
                else:
                    curr_state = 5
                    print_apologies()

        case 3:

            if check_dont_care(user_input, levenshtein_precision):
                stored_preferences[2] = 'any'

            if dialog_act == 'None':
                curr_state = 3
                continue

            restaurant_info = recommend(stored_preferences, already_recommended, random_output)

            if restaurant_info:
                already_recommended.append(restaurant_info)
                curr_state = 4
                print_restaurant(restaurant_info)
            else:
                curr_state = 5
                print_apologies()

        case 4:

            if dialog_act in ['reqalts', 'request', 'reqmore', 'inform']:
                if preferences_changed:
                    restaurant_info = recommend(stored_preferences, already_recommended, random_output)

                    if restaurant_info:
                        already_recommended.append(restaurant_info)
                        curr_state = 4
                        print_restaurant(restaurant_info)
                    else:
                        curr_state = 5
                        print_apologies()
                else:
                    requests = get_user_request(user_input, levenshtein_precision)
                    if requests[0] != None: 
                        print(f'The phone number of the restaurant is {already_recommended[-1][4]}')
                        text_to_speech(f'The phone number of the restaurant is {already_recommended[-1][4]}')
                    if requests[1] != None: 
                        print(f'The address of the restaurant is {already_recommended[-1][5]}')
                        text_to_speech(f'The address of the restaurant is {already_recommended[-1][5]}')
                    if requests[2] != None: 
                        print(f'The post code of the restaurant is {already_recommended[-1][6]}')
                        text_to_speech(f'The post code of the restaurant is {already_recommended[-1][6]}')

                    curr_state = 4
            elif dialog_act in ['thankyou', 'bye']:
                print(bye[0])
                text_to_speech(bye[0])
                exit()
            else:
                print(error[0])
                text_to_speech(error[0])

        case 5:

            if dialog_act in ['thankyou', 'bye']:
                print(bye[0])
                text_to_speech(bye[0])
                exit()

            #this is the same as going to state 1 but without the extra input from the user
            if stored_preferences[1] == None:
                print(ask_area[0])
                text_to_speech(ask_area[0])
                curr_state = 2
            elif stored_preferences[2] == None:
                print(ask_type[0])
                text_to_speech(ask_type[0])
                curr_state = 3
            else:
                restaurant_info = recommend(stored_preferences, already_recommended, random_output)

                if restaurant_info:
                    already_recommended.append(restaurant_info[0])
                    curr_state = 4
                    print_restaurant(restaurant_info)
                else:
                    curr_state = 5
                    print_apologies()



