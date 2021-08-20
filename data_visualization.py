import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

import random

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

for i in range(100, 1, -1):
    time_ms += 100
    objects.append(Object(i, 0, time_ms, 1, True))
    objects.append(Object(random.randrange(0, 100), random.randrange(-10, 10), time_ms, 1, False))


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

pnts_global, = plt.plot([], [], "-bo")
# text_g = plt.text(0, 0, "")
pnts_candidate, = plt.plot([], [], "-ro", mfc='none')

axSlider = plt.axes([0.1, 0.2, 0.8, 0.05])

sldr = Slider(ax=axSlider,
              label="Time",
              valmin=t_0,
              valmax=time_ms,
              valstep=1,
              color="green")

def update_data(val):
    t_prev = t_0
    cur_pack = []
    for pack_ in packs:
        if t_prev < val and val <= pack_.timestamp:
            cur_pack = pack_
        t_prev = pack_.timestamp

    pnts_g = []
    pnts_c = []

    for obj_plot in cur_pack.objects:
        if (obj_plot.is_global):
            pnts_g.append([obj_plot.y, obj_plot.x])
        else:
            pnts_c.append([obj_plot.y, obj_plot.x])

    for pnt in pnts_g:
        pnts_global.set_data(pnt)
    for pnt in pnts_c:
        pnts_candidate.set_data(pnt)
    plt.draw()

sldr.on_changed(update_data)

plt.show()



