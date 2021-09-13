import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import copy

from matplotlib.widgets import Slider

from read_file_data import get_csv_data
from packs_objects import get_packs


def draw():
    objects = get_csv_data('/work/fusion/as_main_module_sf/sensor_fusion3/cmake-build-release/data.csv')
    packs = get_packs(objects)

    fig, ax = plt.subplots()
    plt.grid()
    plt.subplots_adjust(bottom=0.35)
    plt.axis([-50, 50, -1, 150])
    #set steps for every Axis
    x_ticks = np.arange(-50, 50, 10)
    plt.xticks(x_ticks)
    y_ticks = np.arange(0, 150, 10)
    plt.yticks(y_ticks)

    plt.gca().invert_xaxis()
    ax.set_aspect('equal')
    # loc = plticker.MultipleLocator(base=10.0)
    # ax.xaxis.set_major_locator(loc)

    pnts_global, = plt.plot([], [], "bo")
    pnts_candidate, = plt.plot([], [], "ko", mfc='none', alpha=0.1)

    axSlider = plt.axes([0.1, 0.2, 0.8, 0.05])
    sldr = Slider(ax=axSlider,
                  label="Time, sec",
                  valmin=objects[0].time,
                  valmax=objects[-1].time,
                  valstep=0.1,
                  color="green")

    def update_data(val):
        t_prev = objects[0].time
        cur_pack = []
        history_packs = []
        for pack in packs:
            if t_prev < val and val <= pack.timestamp:
                cur_pack = pack
                break

            history_packs.append(pack)
            t_prev = pack.timestamp

        ids = []
        for obj in cur_pack.objects:
            ids.append(obj.id)

        new_history_packs = filter_history(ids, history_packs)

        pnts_g_x = [] #points global Ox
        pnts_g_y = [] #points global Oy
        pnts_c_x = [] #points candidate Ox
        pnts_c_y = [] #points candidate Oy

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

if __name__== "__main__":
  draw()

