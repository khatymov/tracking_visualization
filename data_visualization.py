import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

import random
from matplotlib.animation import FuncAnimation
import copy

class Object:
    def __init__(self, x, y, time, id, is_global):
        self.x = x
        self.y = y
        self.time = time
        self.id = id
        self.is_global = is_global


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

objects = []

time_ms = 10000
t_0 = time_ms

is_global_obj = False

for i in range(100, 40, -1):
    time_ms += 100
    if i < 70:
        is_global_obj = True
    objects.append(Object(i, 0, time_ms, 1, is_global_obj))
    objects.append(Object(i - 20, -10, time_ms, 2, is_global_obj))

is_global_obj = False

for i in range(140, 100, -1):
    time_ms += 100
    if i < 20:
        is_global_obj = True
    objects.append(Object(i, 0, time_ms, 3, is_global_obj))
    objects.append(Object(i - 20, -10, time_ms, 4, is_global_obj))

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


fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)
plt.axis([-25, 25, -1, 150])

pnts_global, = plt.plot([], [], "bo")

pnts_candidate, = plt.plot([], [], "ro", mfc='none')

axSlider = plt.axes([0.1, 0.2, 0.8, 0.05])

sldr = Slider(ax=axSlider,
              label="Time",
              valmin=t_0,
              valmax=time_ms,
              valstep=1,
              color="green")

def filter_history(ids, history):
    new_history = copy.deepcopy(history)
    for pack in new_history:
        i = 0
        del_index = []
        for obj in pack.objects:
            if obj.id not in ids:
                del_index.append(i)

            i += 1

        for j in range(len(del_index), 0, -1):
            pack.objects.pop(j - 1)

    return new_history

def update_data(val):
    t_prev = t_0
    cur_pack = []
    history_packs = []
    for pack_ in packs:
        if t_prev < val and val <= pack_.timestamp:
            cur_pack = pack_
            break

        history_packs.append(pack_)
        t_prev = pack_.timestamp

    ids = []
    for obj in cur_pack.objects:
        ids.append(obj.id)

    new_history_packs = filter_history(ids, history_packs)

    pnts_g_x = []
    pnts_g_y = []
    pnts_c_x = []
    pnts_c_y = []

    for history_pack in new_history_packs:
        for obj_plot in history_pack.objects:
            if (obj_plot.is_global):
                pnts_g_x.append(obj_plot.y)
                pnts_g_y.append(obj_plot.x)
            else:
                pnts_c_x.append(obj_plot.y)
                pnts_c_y.append(obj_plot.x)

    pnts_global.set_data(pnts_g_x, pnts_g_y)
    pnts_candidate.set_data(pnts_c_x, pnts_c_y)

    plt.draw()


sldr.on_changed(update_data)

plt.show()



