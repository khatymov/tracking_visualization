from objects import Object

import csv

def get_csv_data(path):
    objects = []

    #fill data
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) != 5:
                continue
            #x, y, time, id, is_global
            objects.append(Object(float(row[1]), float(row[2]), int(row[0]), int(row[3]), row[4] == "1"))

    objects.sort()

    t_min = objects[0].time

    for obj in objects:
        obj.time = obj.time - t_min
        obj.time = float(obj.time) / 1e6

    return objects
