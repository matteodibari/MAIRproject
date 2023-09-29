import tensorflow as tf
import keras
import numpy as np
import sklearn as sk
from sklearn import model_selection
from sklearn import metrics
from keras import layers

# import the enchant module
import enchant
import math

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


dontCareLoc = ["anyplace", "anypart", "anyarea"]
dontCarePrice = ["anyprice"]
dontCareRest = ["anyfood", "anykind", "anytype"]
sentense1 = "Im looking for an Expensive restaurant that serves asianoriental and north yes"
sentense2 = "pan asian"
sentense3 = "m o d e r a  t ly priced restaurant in the south part of town"
sentense4 = "I'm looking for a restaurant in any area that serves Tuscan food"

def compareSets(set1, set2):
    for type in set1:
        index = - 1
        allPref= []
        for letter in set2:
            #print(letter)
            index = index + 1
            if letter == type[0] and index + len(type) < len(set2) + 1:
                sub = set2[index: index + len(type)]

                diff = enchant.utils.levenshtein(type, sub)
                if diff < math.floor(len(type) / 5):
                    if type == 'asian':
                        type = 'asian oriental'
                    return type
                    print(sub, type)
                    #allPref.append(type)
    #return allPref

def getUserPref(sentence):
    sentence = sentence.replace(" ", "")
    sentence = sentence.lower()
    allPref = []
    #print(sentence)
    allPref.append(compareSets(priceTypes, sentence))
    allPref.append(compareSets(locationTypes, sentence))
    allPref.append(compareSets(restaurantTypes, sentence))
    if allPref[0] is None:
        if compareSets(dontCarePrice, sentence) is not None:
            allPref[0] = "any"
    if allPref[1] is None:
        if compareSets(dontCareLoc, sentence) is not None:
            allPref[1] = "any"
    if allPref[2] is None:
        if compareSets(dontCareRest, sentence) is not None:
            allPref[2] = "any"
    return allPref



print(getUserPref(sentense4))
#getUserPref(sentense2)
#getUserPref(sentense3)

i = 0
import csv
if "area" in ['"restaurantname"', '"pricerange"', '"area"', '"food"', '"phone"', '"addr"', '"postcode"']:
    print('da')
if '"area"' in ['"restaurantname"', '"pricerange"', '"area"', '"food"', '"phone"', '"addr"', '"postcode"']:
    print('da')
#if ('\"' + pref + '\"') in ['"pizza express fen ditton"', '"moderate"', '"centre"', '"european"', '""', '"jesus lane fen ditton"', '""']:

def recommend(allPref):
    matchesNeeded = 3
    userPref = []
    for pref in allPref:
        if pref == 'any' or pref is None:
            matchesNeeded = matchesNeeded - 1

    with open('restaurant_info.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')

        for row in spamreader:
            #print(row)
            score = 0
            for pref in allPref:
                #print(pref, row)
                if pref in row:
                    #print('hi')
                    score = score + 1
            if score == matchesNeeded:

                userPref.append(row[0])
                for i in range(3):
                    if allPref[i] == 'any':
                        userPref.append('any')
                    elif allPref[i] is None:
                        userPref.append("unknown")
                    else:
                        userPref.append(row[i + 1])
    return userPref


print(recommend(getUserPref(sentense1)))
print(recommend(getUserPref(sentense4)))
pref = recommend(getUserPref(sentense1))
print('The perfect restaurant is ' + pref[0] + ' with ' + pref[1] + ' price range which is located in ' + pref [2] + ' part of the town and serve ' + pref[3] + ' food')
pref = recommend(getUserPref(sentense4))
print('The perfect restaurant is ' + pref[0] + ' with ' + pref[1] + ' price range which is located in ' + pref [2] + ' part of the town and serve ' + pref[3] + ' food')