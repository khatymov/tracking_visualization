import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


class Object:
    def __init__(self, x, y, time, id):
        self.x = x
        self.y = y
        self.time = time
        self.id = id


objects = []

time_ms = 1662832
t_0 = time_ms

for i in range(100, 1, -1):
    time_ms += 100
    objects.append(Object(i, 0, time_ms, 1))


x = []
y = []
ids = []

for obj in objects:
    x.append(obj.x)
    y.append(obj.y)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)
plt.axis([-25, 25, -1, 150])

p, = plt.plot(y, x, "-bo")

axSlider = plt.axes([0.1, 0.2, 0.8, 0.05])

sldr = Slider(ax     = axSlider,
              label  = "Time",
              valmin = 0,
              valmax = time_ms - t_0,
              color  = "green")

def update_data(val):
    y_val = sldr.val
    p.set_ydata(y_val)
    plt.draw()

sldr.on_changed(update_data)

plt.show()



