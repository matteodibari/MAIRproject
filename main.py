import numpy as np
from keras.models import load_model
from model_feed_forward import sentence_to_vector_2
from model_feed_forward import vector_to_label
from model_feed_forward import to_one_hot
from userpref import get_user_pref
from userpref import recommend
from userpref import get_user_request
from userpref import check_dont_care

curr_state = 1
#this variable keeps track of the current state during the state transitioning algorithm

stored_preferences = [None, None, None]
#stored-preferences = [price-range, area, type]

ask_area = ['In which area are you searching for the restaurant?']
ask_type = ['Which type of food are you searching for?']
bye = ['Goodbye!']
error = ['Sorry, I did not understand what you meant.']


def print_aditional_info(aditional_info):
    """
    This function prints information about the best restaurant in a user-friendly manner.
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

def print_restaurant(restaurant_info):
    """
    This function prints the suggestion given the information of a restaurant.

    :param restaurant_info: information of the restaurant.
    """

    if len(restaurant_info) == 1:
        print('Sorry, there is no restaurant with these requirements.')
        return
    
    print('The perfect restaurant is ' + restaurant_info[0] + ' with ' + restaurant_info[1] + 
                          ' price range which is located in ' + restaurant_info [2] + ' part of the town and serves ' 
                          + restaurant_info[3] + ' food.')
    print_aditional_info(restaurant_info)

    return


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


    #y = model.predict(np.array([sentence_to_vector_2('goodbye', words)]))
    y = model.predict( np.array( [sentence_to_vector_2(input_msg, words),] ), verbose=0)
    y = to_one_hot(y[0])
    return vector_to_label(y)

def print_apologies():
    """
    This function prints the apologies given the current user preferences.
    """

    print(f'Sorry, I did not find any restaurant matching these preferences: {stored_preferences[0]}, {stored_preferences[1]}, {stored_preferences[2]}. Please search again.')


#list of already recommended restaurant (list of arrays)
already_recommended = []

print('Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?')

while(1):
    user_input = input()
    dialog_act = predict_dialog_act(user_input)
    print(dialog_act)

    if dialog_act == 'restart':
        print('System restarting...')
        stored_preferences = [None, None, None]
        already_recommended = []
        print('Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?')
        curr_state = 1
        continue

    preferences_changed = False

    #clearing the preferences if we entered in state 5
    if curr_state == 5: 
        stored_preferences = [None, None, None]

    preferences = get_user_pref(user_input)
    # preferences[3] = [price, location, typeoffood]

    for i in range(len(stored_preferences)):
        if preferences[i] != None: 
            stored_preferences[i] = preferences[i]
            preferences_changed = True

    match curr_state:
        case 1:
            
            if stored_preferences[1] == None: 
                print(ask_area[0])
                curr_state = 2
            elif stored_preferences[2] == None:
                print(ask_type[0])
                curr_state = 3
            else:
                restaurant_info = recommend(stored_preferences, already_recommended)
                
                if restaurant_info:
                    already_recommended.append(restaurant_info)
                    curr_state = 4
                    print_restaurant(restaurant_info)
                else:
                    curr_state = 5
                    print_apologies()
        case 2:
            
            if check_dont_care(user_input):
                stored_preferences[1] = 'any'

            if dialog_act == 'None':
                curr_state = 2
                continue

            if stored_preferences[2] == None:
                print(ask_type[0])
                curr_state = 3
            else:
                restaurant_info = recommend(stored_preferences, already_recommended)
                
                if restaurant_info:
                    already_recommended.append(restaurant_info)
                    curr_state = 4
                    print_restaurant(restaurant_info)
                else:
                    curr_state = 5
                    print_apologies()

        case 3:

            if check_dont_care(user_input):
                stored_preferences[2] = 'any'
            
            if dialog_act == 'None':
                curr_state = 3
                continue
            
            restaurant_info = recommend(stored_preferences, already_recommended)

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
                    restaurant_info = recommend(stored_preferences, already_recommended)

                    if restaurant_info:
                        already_recommended.append(restaurant_info)
                        curr_state = 4
                        print_restaurant(restaurant_info)
                    else:
                        curr_state = 5
                        print_apologies()
                else:
                    requests = get_user_request(user_input)
                    if requests[0] != None: print(f'The phone number of the restaurant is {already_recommended[-1][4]}')
                    if requests[1] != None: print(f'The address of the restaurant is {already_recommended[-1][5]}')
                    if requests[2] != None: print(f'The post code of the restaurant is {already_recommended[-1][6]}')

                    curr_state = 4
            elif dialog_act in ['thankyou', 'bye']:
                print(bye[0])
                exit()
            else:
                print(error[0])  

        case 5:

            if dialog_act in ['thankyou', 'bye']:
                print(bye[0])
                exit()

            #this is the same as going to state 1 but without the extra input from the user
            if stored_preferences[1] == None: 
                print(ask_area[0])
                curr_state = 2
            elif stored_preferences[2] == None:
                print(ask_type[0])
                curr_state = 3
            else:
                restaurant_info = recommend(stored_preferences, already_recommended)
                
                if restaurant_info:
                    already_recommended.append(restaurant_info[0])
                    curr_state = 4
                    print_restaurant(restaurant_info)
                else:
                    curr_state = 5
                    print_apologies()
        
    # print(curr_state)




