# MAIR project

This project implements a dialog system for restaurant recommendations. It uses a database of restaurants and it is based on a Feed Forward Model that is capable of recognising the dialog act relative to the user input.

## How tho run it?
To open the dialog system it is necessary to run the main.py file, which will start the chatbot. 

## How to use?
You are first asked to add customizations to the system. Typing no will set the chatbot to use the default settings. 
Typing yes will let you firstly choose wheter you want the restaurant suggestions to be given in random order, and secondly choose the level of precision for the Levenshtein distance (measure of similarity between words used for word recognition).
Then you are asked to choose the way you prefer to input the messages. Typing 1 will set the default user input to keyboard, while typing 2 will set the default input to microphone (the system will then use a speech-to-text engine to formulate your requests).
Then the chatbot will start with a welcome utterance, you will then be able to request a restaurant based on location in the city, price range, and type of food. 
After the first informations are given the system will ask for any additional requirements. The available options are: assigned seats, romantic, children allowed and touristic.
Finally it will find a valid suggestion from the database, from which you can stop the chatbot simply saying 'bye' or you can modify your preferences and search for other options.

## Dialog examples

### baseline_1.py
This file implements a system that, given an input utterance, returns the label 'inform', which is the majority class of the used dataset.

### baseline_1.py
This one instead uses a word-matching algorithm to assign a label to the given sentence. For example if the word 'more' is found, the assigned label will be 'reqmore', and so on.

### decision_tree.py
Implementation of a Decision Tree Classifier capable of recognising the dialog act given a sentence.

### main.py
This file is the core of the project. It contains the state transitioning function.

### model_feed_forward.py
Implementation of a Feed Forward Model capable of recognising the dialog act given a sentence.

### text_speech.py
This file implements the functions used for the speech-to-text and text-to-speech features of the chatbot.

### user_pref.py
This file implements the major functions of the system, such as the recommendation of a restaurant given the preferences or the keyword matching algorithm to find keywords in the user sentence (based on Levenshtein distance).

## saved_model.h5
This files contains the weights of a trained Feed Forward Model and can be loaded using keras method 'load_model()'


