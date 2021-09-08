
class Object:
    def __init__(self, x, y, time, id, is_global):
        self.x = x
        self.y = y
        self.time = time
        self.id = id
        self.is_global = is_global

    def __lt__(self, other):
        return self.time < other.time

class PackObjects:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.objects = []

    def append(self, obj):
        self.objects.append(obj)
        self.timestamp = obj.time

    def clear(self):
        self.objects.clear()
        self.timestamp = 0