
class Object:
    def __init__(self, x, y, time, id, is_global):
        self.x = x
        self.y = y
        self.time = time
        self.id = id
        self.is_global = is_global

    def __lt__(self, other):
        return self.time < other.time

