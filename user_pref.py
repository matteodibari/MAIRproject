from enchant import utils
import math
import csv
import random

#the following lines define the keywords used for preference matching

restaurant_types = ["british", "european", "italian", "romanian", "seafood", "chinese", "steakhouse", "moderneuropean", "french", "asian", "portuguese", "indian", "spanish", "vietnamese", "european", "korean", "thai", "moroccan", "swiss", "gastropub", "fusion", "tuscan", "international", "traditional", "polynesian", "turkish", "african", "mediterranian", "bistro", "northamerican", "australian", "persian", "jamaikan", "lebanese", "cuban", "japanese", "catalan"]
price_types = ["expensive", "moderate", "cheap"]
location_types = ["south", "west", "centre", "east", "north"]

dont_care_loc = ["anyplace", "anypart", "anyarea"]
dont_care_price = ["anyprice"]
dont_care_rest = ["anyfood", "anykind", "anytype"]

post_code_keywords = ["postalcode", "postcode"]
phone_keywords = ["contact", "phone"]
address_keywords= ["address", "located"]

additional_infos = ['touristic', 'assignedseats', 'children', 'romantic']

def compare_sets(keywords, sentence, precision):
    """
    This function uses Levenshtein distance to find keyword matches inside a sentence.

    :param types: keywords.
    :param sentence: sentence to use for the matching.
    :param precision: Precision of the Levinstein edit diatance.
    :return keyword: first matching keyword.
    """
    for keyword in keywords:
        index = 0
        for letter in sentence:
            # checking the first letter that matches the first letter of the keyword and
            # checking if the keyword fits the rest of the sentence
            if letter == keyword[0] and index + len(keyword) < len(sentence) + 1:
                sub = sentence[index: index + len(keyword)]
                dinstance = utils.levenshtein(keyword, sub)
                if dinstance <= math.floor(len(keyword) / precision):
                    if keyword == 'asian':
                        keyword = 'asian oriental'
                    return keyword
            index += 1


def get_user_pref(sentence, precision):
    """
    This function checks for any keywords in a sentence using the compare_sets function.
    Moreover it checks for the user does not have a preference, in which case it fills
    the corresponding field with 'any'.

    :param sentence: sentence to use for the keyword matching.
    :param precision: Precision of the Levinstein edit diatance.
    :return: list with preferences for price, location and food.
    """
    sentence = sentence.replace(" ", "")
    sentence = sentence.lower()

    all_pref = []
    all_pref.append(compare_sets(price_types, sentence, precision))
    all_pref.append(compare_sets(location_types, sentence, precision))
    all_pref.append(compare_sets(restaurant_types, sentence, precision))

    if all_pref[0] is None:
        if compare_sets(dont_care_price, sentence, precision) is not None:
            all_pref[0] = "any"
    if all_pref[1] is None:
        if compare_sets(dont_care_loc, sentence, precision) is not None:
            all_pref[1] = "any"
    if all_pref[2] is None:
        if compare_sets(dont_care_rest, sentence, precision) is not None:
            all_pref[2] = "any"
    return all_pref


def get_user_request(sentence, precision):
    """
    A function that checks for requests about phone number, post code or address.

    :param sentence: the sentence in which we will search preferences.
    :param precision: Precision of the Levinstein edit diatance.
    :return: list with requests for phone, address and post code.
    """
    sentence = sentence.replace(" ", "")
    sentence = sentence.lower()

    all_pref = []
    all_pref.append(compare_sets(phone_keywords, sentence, precision))
    all_pref.append(compare_sets(address_keywords, sentence, precision))
    all_pref.append(compare_sets(post_code_keywords, sentence, precision))

    return all_pref


def recommend(all_pref, already_recommended, randomOutput, all=False):
    """
    The function finds the best possible restaurant, based on the preferences of the user
    and the additional preferences that are asked separately. First, the function finds the
    number of needed matches for requirements which removes 'any's and 'None's. Then reads
    all the restaurants from the database and checks for the number of matches.

    :param all_pref: all user preferences.
    :param already_recommended: list with all already recommended restaurants.
    :param randomOutput: Parameter for listing restaurants in random order.
    :param all: if this param is true the function returns a list of all the possible restaurants.
    :return restaurant: the whole line of the database relative to the recommended restaurant.
    """

    possible_restaurants, additional_request = recommend_additional_info()
    matches_needed = 3
    user_pref = []
    for pref in all_pref:
        if pref == 'any' or pref is None:
            matches_needed = matches_needed - 1
    all_restaurants = []

    with open('restaurant_info.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')

        for row in spamreader:
            score = 0
            for pref in all_pref:
                if pref in row:
                    score = score + 1
                if pref == 'asian oriental' and 'asian' in row:
                    score = score + 1
            if score == matches_needed and row not in already_recommended[:]:
                if possible_restaurants is None:
                    possible_restaurants = row[0]
                if row[0] in possible_restaurants:
                    user_pref.append(row[0])
                    for i in range(3):
                        if all_pref[i] == 'any':
                            user_pref.append('any')
                        elif all_pref[i] is None:
                            user_pref.append("unknown")
                        else:
                            user_pref.append(row[i + 1])
                    user_pref.extend(row[4:10])
                    if all == False and randomOutput != 'yes':
                        break
                all_restaurants.append(row)

    if all == False:
        if randomOutput == 'yes':
            index = random.randint(0, len(all_restaurants) - 1)
            all_restaurants[index].append(additional_request)
            return all_restaurants[index]
        user_pref.append(additional_request)
        return user_pref
    return all_restaurants


def check_dont_care(sentence, precision):
    """
    This function checks for any dont care statements in a sentence.

    :param sentence: input sentence.
    :param precision: Precision of the Levinstein edit diatance.
    :return: True or False for containing don't care statement.
    """

    sentence = sentence.replace(" ", "")
    sentence = sentence.lower()
    if compare_sets(['dontcare', 'doesntmatter', 'doesnotmatter', 'donotcare', 'nopreference'], sentence, precision):
        return True
    else:
        return False


def recommend_additional_info(precision=5):
    """
    This function takes a sentence from standard input and it searches for
    preferences about the place (good for children, romantic, etc.) and gives a
    list of possible restaurants.

    :param precision: Precision of the Levinstein edit diatance.
    :return: list of possible restaurants and users preferences.
    """

    sentence = input("Do you have additional requirements?\n")

    if sentence == "No":
        return None, None

    possible_restaurants = []
    userpref = compare_sets(additional_infos, sentence, precision)

    with open('restaurant_info.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        for row in spamreader:
            if len(row) < 1:
                continue
            if userpref == 'touristic' and row[1] == 'cheap' and row[7] == 'good' and row[2] != 'romanian':
                possible_restaurants.append(row[0])
            if userpref == 'assignedseats' and row[8] == 'busy':
                possible_restaurants.append(row[0])
            if userpref == 'children' and row[9] != 'long time':
                possible_restaurants.append(row[0])
            if userpref == 'romantic' and row[8] != 'busy' and row[9] == 'long time':
                possible_restaurants.append(row[0])

    if len(possible_restaurants) == 0:
        possible_restaurants = None
        userpref = None

    return possible_restaurants, userpref
