# from objects import PackObjects

class PackObjects:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.objects = []

    def append(self, obj):
        self.objects.append(obj)
        self.timestamp = obj.timestamp

    def clear(self):
        self.objects.clear()
        self.timestamp = 0


def get_packs(objects, time_frame_use, ts_start, ts_end):
    packs = []
    cur_time = objects[0].timestamp

    pack = PackObjects(cur_time)

    for obj in objects:
        if time_frame_use and (ts_start > obj.timestamp or obj.timestamp > ts_end):
            cur_time = obj.timestamp
            continue
        if cur_time == obj.timestamp:
            pack.append(obj)
        else:
            pack.timestamp = cur_time
            packs.append(pack)
            pack = PackObjects(cur_time)
            pack.append(obj)
            cur_time = obj.timestamp

    return packs