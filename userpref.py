import tensorflow as tf
import keras
import csv
import numpy as np
import sklearn as sk
from sklearn import model_selection
from sklearn import metrics
from keras import layers

# import the enchant module
import enchant
#from enchant import utils

# determining the values of the parameters
string1 = "Hello World"
string2 = "Hello d"

# the Levenshtein distance between
# string1 and string2
print(enchant.utils.levenshtein(string1, string2))

restaurantTypes = ["british", "european", "italian", "romanian", "seafood", "chinese", "steakhouse", "moderneuropean", "french", "asian", "portuguese", "indian", "spanish", "vietnamese", "european", "korean", "thai", "moroccan", "swiss", "gastropub", "fusion", "tuscan", "international", "traditional", "polynesian", "turkish", "african", "mediterranian", "bistro", "northamerican", "australian", "persian", "jamaikan", "lebanese", "cuban", "japanese", "catalan"]
priceTypes = ["expensive", "moderate", "cheap"]
locationTypes = ["south", "west", "centre", "east", "north"]
sentense1 = "Im looking for an Expensive restaurant that serves asianoriental"
sentense2 = "pan asian"
sentense3 = "m o d e r a  t ly priced restaurant in the south part of town"

def compareSets(set1, set2):
    for type in set1:
        index = - 1
        for letter in set2:
            #print(letter)
            index = index + 1
            if letter == type[0] and index + len(type) < len(set2) + 1:
                sub = set2[index: index + len(type)]

                diff = enchant.utils.levenshtein(type, sub)
                if diff < 2:
                    if type == 'asian':
                        type = 'asian oriental'
                    print(sub, type)

def getUserPref(sentence):
    sentence = sentence.replace(" ", "")
    sentence = sentence.lower()
    #print(sentence)
    compareSets(priceTypes, sentence)
    compareSets(locationTypes, sentence)
    compareSets(restaurantTypes, sentence)

getUserPref(sentense1)
getUserPref(sentense2)
getUserPref(sentense3)



with open('restaurant_info.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(row)


while(1):
    input_msg = input()
    output_msg = ''
    print(output_msg)