# from objects import PackObjects

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


def get_packs(objects):
    packs = []
    cur_time = objects[0].time

    pack = PackObjects(cur_time)

    for obj in objects:
        if cur_time == obj.time:
            pack.append(obj)
        else:
            pack.timestamp = cur_time
            packs.append(pack)
            pack = PackObjects(cur_time)
            pack.append(obj)
            cur_time = obj.time

    return packs