
class Object:
    def __init__(self, time, x, y, id, is_global):
        self.time = time
        self.x = x
        self.y = y
        self.id = id
        self.is_global = is_global

    def __lt__(self, other):
        return self.time < other.time

