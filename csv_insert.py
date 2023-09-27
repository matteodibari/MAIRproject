import csv
import random
import tempfile
import shutil

def restaurant_info_insert():
    with open('data/restaurant_info.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # create 3 new colum
    colum_food = ["food quality"]
    colum_crowd = ["crowdedness"]
    colum_stay = ["length of stay"]

    # set the range of new colum
    food_range = ["good", "bad"]
    crowd_range = ["busy", "not busy"]
    stay_range = ["long time", "short time"]

    # finish 3 colum
    for i1 in range(len(data)-1):
        colum_food.append(random.choice(food_range))
        colum_crowd.append(random.choice(crowd_range))
        colum_stay.append(random.choice(stay_range))

    # print(colum_food)

    # insert the new colum into data
    for i2 in range(len(data)):
        data[i2].append(colum_food[i2])
        data[i2].append(colum_crowd[i2])
        data[i2].append(colum_stay[i2])

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        writer = csv.writer(temp_file)
        writer.writerows(data)
        temp_file_path = temp_file.name

    # copy and replace the data in csv file
    shutil.move(temp_file_path, 'G:/MLproject/p_01/data/restaurant_info.csv')
    print("Insert complete!")


restaurant_info_insert()
