import tensorflow as tf
import keras
import numpy as np
import sklearn as sk
from sklearn import model_selection
from sklearn import metrics
from keras import layers

# import the enchant module
from enchant import utils
import math
import csv


restaurantTypes = ["british", "european", "italian", "romanian", "seafood", "chinese", "steakhouse", "moderneuropean", "french", "asian", "portuguese", "indian", "spanish", "vietnamese", "european", "korean", "thai", "moroccan", "swiss", "gastropub", "fusion", "tuscan", "international", "traditional", "polynesian", "turkish", "african", "mediterranian", "bistro", "northamerican", "australian", "persian", "jamaikan", "lebanese", "cuban", "japanese", "catalan"]
priceTypes = ["expensive", "moderate", "cheap"]
locationTypes = ["south", "west", "centre", "east", "north"]


dontCareLoc = ["anyplace", "anypart", "anyarea"]
dontCarePrice = ["anyprice"]
dontCareRest = ["anyfood", "anykind", "anytype"]

postCodeKeyWords = ["postalcode", "postcode"]
phoneKeyWords = ["contact", "phone"]
addressKeyWords= ["address", "located"]


sentense1 = "Im looking for an Expensive restaurant that serves asianoriental and north yes"
sentense2 = "pan asian north "
sentense3 = "m o d e r a  t ly priced restaurant in the south part of town"
sentense4 = "I'm looking for a restaurant in any area that serves Tuscan food"
sentense5 = "I would like the restaurant to be romantic"
sentense6 = "uh whats the phone number and address please"



def compareSets(types, sentence):
    """
    This function take two arrrays. First one will be possible types of location price or food
    and the second one will be the sentence. The function check levenshtein distance  of each type
    on every subarray with the same length of it from the sentence and return the firrst match.
    The distance should be less or equal to the length of the word so we can still catch wrong writen
    longer words and also keep the accuracy good for

    :param set1: First set to compare
    :param sentence: Second set to comapare
    :return: The first instance of an element in set
             one that has small enough levenshtein distance with eleement in set two.
    """
    for type in types:
        index = - 1
        for letter in sentence:
            index = index + 1
            if letter == type[0] and index + len(type) < len(sentence) + 1:
                sub = sentence[index: index + len(type)]

                diff = utils.levenshtein(type, sub)
                if diff <= math.floor(len(type) / 5):
                    if type == 'asian':
                        type = 'asian oriental'
                    return type


def getUserPref(sentence):
    """
    This function check the sentence for all keywords about type of food, location and price.
    Then matches keywords for dont care and fill them ontho the needed places.

    :param sentence: The sentence in which we weill search preferences
    :return: list with preferences for price, location and food
    """
    sentence = sentence.replace(" ", "")
    sentence = sentence.lower()

    allPref = []
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

def checkDontCare(sentence):
    sentence = sentence.replace(" ", "")
    sentence = sentence.lower()
    if compareSets(['dontcare', 'doesntmatter', 'doesnotmatter', 'donotcare', 'nopreference'], sentence):
        return True
    else: 
        return False

def getUserRequest(sentence):
    sentence = sentence.replace(" ", "")
    sentence = sentence.lower()

    allPref = []
    allPref.append(compareSets(phoneKeyWords, sentence))
    allPref.append(compareSets(addressKeyWords, sentence))
    allPref.append(compareSets(postCodeKeyWords, sentence))

    return allPref

def recommend(allPref, already_recommended, all=False):
    matchesNeeded = 3
    userPref = []
    for pref in allPref:
        if pref == 'any' or pref is None:
            matchesNeeded = matchesNeeded - 1
    allRestaurants = []

    with open('restaurant_info.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')

        for row in spamreader:
            score = 0
            for pref in allPref:
                if pref in row:
                    score = score + 1
                if pref == 'asian oriental' and 'asian' in row:
                    score = score + 1
                if pref == None:
                    score = score + 1
            if score == matchesNeeded and row not in already_recommended[:]:            
                userPref.append(row[0])
                for i in range(3):
                    if allPref[i] == 'any':
                        userPref.append('any')
                    elif allPref[i] is None:
                        userPref.append("unknown")
                    else:
                        userPref.append(row[i + 1])
                userPref.extend(row[4:7])
                if all == False:
                    break
                allRestaurants.append(row[0])
                
    if all == False:
        return userPref
    return allRestaurants

keyWords = ['touristic', 'assignedseats', 'children', 'romantic']

def aditionalInfoRecommend(sentence, lastSentence):
    posibleRestaurants = recommend(getUserPref(lastSentence), True)
    userpref = compareSets(keyWords, sentence)

    with open('restaurant_info.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')

        for row in spamreader:
            if len(row) < 1:
                continue
            if userpref == 'turistc' and row[1] == 'cheap' and row[7] == 'good' and row[2] != 'romanian' and row[0] in posibleRestaurants:
                return row
            if userpref == 'assignedseats' and row[8] == 'busy' and row[0] in posibleRestaurants:
                return row
            if userpref == 'children' and row[9] != 'long time' and row[0] in posibleRestaurants:
                return row
            if userpref == 'romantic' and row[8] != 'busy' and row[9] == 'long time' and row[0] in posibleRestaurants:
                return row
