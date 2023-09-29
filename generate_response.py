import numpy as np
from keras.models import load_model
from model_feed_forward import sentence_to_vector_2
from model_feed_forward import vector_to_label
from model_feed_forward import to_one_hot
from userpref import getUserPref
from userpref import recommend


curr_state = 1

#stored-data = [price-range, area, type]
stored_preferences = [None, None, None]

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

y = model.predict( np.array( [sentence_to_vector_2('what is happening', words)] ))
y = to_one_hot(y[0])
print(y)
print(vector_to_label(y))



#print('Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?')

def print_restaurant(restaurant_info):
    print('The perfect restaurant is ' + restaurant_info[0] + ' with ' + restaurant_info[1] + 
                          ' price range which is located in ' + restaurant_info [2] + ' part of the town and serve ' 
                          + restaurant_info[3] + ' food')
    return


# while(1):
#     user_input = input()
#     dialog_act = 'thankyou'

#     preferences = getUserPref(user_input)
#     # preferences[3] = [price, location, typeoffood]

#     for i in range(len(stored_preferences)):
#         if stored_preferences[i] == None: stored_preferences[i] = preferences[i]

#     print(stored_preferences)


#     match curr_state:
#         case 1:
#             print('sys just entered state 1')
#             if stored_preferences[1] == None: 
#                 print(ask_area[0])
#                 curr_state = 2
#             elif stored_preferences[2] == None:
#                 print(ask_type[0])
#                 curr_state = 3
#             else:
#                 restaurant_info = recommend(stored_preferences)
#                 #restaurant_info[4] = [restaurant, price, location, typeoffood]
                
#                 if restaurant_info:
#                     curr_state = 4
#                     print_restaurant(restaurant_info)
#                 else:
#                     curr_state = 5
#                     print(apologies[0])
#         case 2:
#             print('sys just entered state 2')
#             if dialog_act == 'None':
#                 curr_state = 2
#                 continue

#             if stored_preferences[2] == None:
#                 print(ask_type[0])
#                 curr_state = 3
#             else:
#                 restaurant_info = recommend(stored_preferences)
#                 if restaurant_info:
#                     curr_state = 4
#                     print_restaurant(restaurant_info)
#                 else:
#                     curr_state = 5
#                     print(apologies[0])

#         case 3:
#             print('SYSTEM: just entered state 3')
#             if dialog_act == 'None':
#                 curr_state = 3
#                 continue
            
#             restaurant_info = recommend(stored_preferences)
#             print(restaurant_info)

#             if restaurant_info:
#                 curr_state = 4
#                 print_restaurant(restaurant_info)
#             else:
#                 curr_state = 5
#                 print(apologies[0])

#         case 4:
#             if dialog_act == 'reqalts':
#                 restaurant_info = recommend(stored_preferences)
#                 if restaurant_info:
#                     curr_state = 4
#                     print_restaurant(restaurant_info)
#                 else:
#                     curr_state = 5
#                     print(apologies[0])

#             elif dialog_act in ['request', 'reqmore']:
#                 # search for the infos
#                 # give the info
#                 curr_state = 7

#             elif dialog_act == 'thankyou':
#                 print(bye[0])
#                 exit()

#             else:
#                 if dialog_act == 'repeat':
#                     continue
#                 else:
#                     print(error[0])          

#         case 5:
#             if stored_preferences[0] == None: 
#                 curr_state = 2
#             elif stored_preferences[1] == None:
#                 curr_state = 3
#             else:
#                 restaurant_info = recommend(stored_preferences)
#                 if restaurant_info:
#                     curr_state = 4
#                     print_restaurant(restaurant_info)
#                 else:
#                     curr_state = 5
#                     print(apologies[0])




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
  
