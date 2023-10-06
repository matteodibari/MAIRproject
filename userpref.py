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

def compareSets(types, sentence):
    """
    This function takes two arrays. The first one will be possible types of location price or food
    and the second one will be the sentence. The function checks the Levenshtein distance of each type
    on every subarray with the same length of it from the sentence and returns the first match.
    The distance should be comparable to the length of the word so we can still catch wrong-written
    longer words and also keep the accuracy good for short ones.

    :param set1: First set to compare
    :param sentence: Second set to comapare
    :return: The first instance of an element in the set
             one that has a small enough Levenshtein distance with element in set two.
    """
    for type in types:
        index = - 1
        for letter in sentence:
            index = index + 1
            if letter == type[0] and index + len(type) < len(sentence) + 1:
                sub = sentence[index: index + len(type)]

                diff = enchant.utils.levenshtein(type, sub)
                if diff <= math.floor(len(type) / 5):
                    if type == 'asian':
                        type = 'asian oriental'
                    return type


def getUserPref(sentence):
    """
    This function checks the sentence for all keywords about the type of food, location and price.
    Then match keywords for don't care and fill them in the needed places.

    :param sentence: The sentence in which we will search preferences.
    :return: List with preferences for price, location and food.
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

def getUserRequest(sentence):
    """
    A function that checks for requests about phone number, post code or address.
    :param sentence: The sentence in which we will search preferences.
    :return: List with requests for phone, address and post code.
    """
    sentence = sentence.replace(" ", "")
    sentence = sentence.lower()

    allPref = []
    allPref.append(compareSets(phoneKeyWords, sentence))
    allPref.append(compareSets(addressKeyWords, sentence))
    allPref.append(compareSets(postCodeKeyWords, sentence))

    return allPref




def recommend(allPref, already_recommended, all=False):
    """
    The function finds the best possible restaurant, based on the preference of the use
    and the additional preferences that are asked separately. First, the function finds the
    number of needed matches for requirements which removes anys and Nones. Then read
    all the restaurants from the database and check for the number of matches.
    :param allPref: All preferences of the user
    :param already_recommended: List will all already recommended restaurants.
    :param all: Should we return all possible restaurants or only one
    :return: The whole line of the database with all the info and the type of additional request.
    """
    posibleRestaurants, additionalRequest = aditionalInfoRecommend()
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
                #This is just to handle empty aditional requrements
                if posibleRestaurants is None:
                    posibleRestaurants = row[0]
                if row[0] in posibleRestaurants:
                    userPref.append(row[0])
                    for i in range(3):
                        if allPref[i] == 'any':
                            userPref.append('any')
                        elif allPref[i] is None:
                            userPref.append("unknown")
                        else:
                            userPref.append(row[i + 1])
                    userPref.extend(row[4:10])
                    if all == False:
                        break
                allRestaurants.append(row[0])

    if all == False:
        userPref.append(additionalRequest)
        return userPref
    return allRestaurants


def checkDontCare(sentence):
    """
    This function just checks for any dont care statements in a sentence.
    :param sentence: Input sentence
    :return: True or False for containing don't care statement
    """
    sentence = sentence.replace(" ", "")
    sentence = sentence.lower()
    if compareSets(['dontcare', 'doesntmatter', 'doesnotmatter', 'donotcare', 'nopreference'], sentence):
        return True
    else:
        return False



keyWords = ['touristic', 'assignedseats', 'children', 'romantic']

def aditionalInfoRecommend():
    """
    This function takes an input statement from the user and from it finds
    preferences about the place like good for children or romantic and makes a
    list of possible restaurants.
    :return: List of possible restaurants and users preferences.
    """
    sentence = input("Do you have additional requirements?")
    if sentence == "No":
        return None, None

    posibleRestaurants = []
    userpref = compareSets(keyWords, sentence)

    with open('restaurant_info.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')

        for row in spamreader:
            if len(row) < 1:
                continue
            if userpref == 'turistc' and row[1] == 'cheap' and row[7] == 'good' and row[2] != 'romanian':
                posibleRestaurants.append(row[0])
            if userpref == 'assignedseats' and row[8] == 'busy':
                posibleRestaurants.append(row[0])
            if userpref == 'children' and row[9] != 'long time':
                posibleRestaurants.append(row[0])
            if userpref == 'romantic' and row[8] != 'busy' and row[9] == 'long time':
                posibleRestaurants.append(row[0])
    if len(posibleRestaurants) == 0:
        return None, None
    return posibleRestaurants, userpref

