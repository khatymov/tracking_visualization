
class Object:
    def __init__(self, time, x, y, id, id_class, is_global, ch_counter):
        self.timestamp = time
        self.x = x
        self.y = y
        self.id = id
        self.is_measurement = bool(id == -1)
        self.id_class = id_class
        self.is_global = is_global
        self.channel_cntr = ch_counter
        self.old_ts = 0

    def __lt__(self, other):
        return self.timestamp < other.timestamp

ObjectClass = {0:"UNDEF",
               1:"PERSON",
               2:"TRAIN",
               3:"AUTO",
               4:"ANIMAL",
               5:"INFRA",
               6:"OTHER"}