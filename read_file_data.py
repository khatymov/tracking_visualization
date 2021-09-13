from objects import Object

import csv

def get_csv_data(path):
    objects = []

    #fill data
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) < 6 or row[0] == "ts":
                print(row)
                continue
            #ts, x, y, id, id_class, is_global, ,channel_0, counter_0, channel_1, counter_1, ..
            objects.append(Object(int(row[0]), float(row[1]), float(row[2]), int(row[3]), int(row[4]), row[5] == "1", row[7:]))

    objects.sort()

    t_min = objects[0].timestamp

    for obj in objects:
        obj.old_ts = obj.timestamp
        obj.timestamp = obj.timestamp - t_min
        obj.timestamp = float(obj.timestamp) / 1e6

    return objects

