import matplotlib.pyplot as plt
import numpy as np
import copy

from matplotlib.widgets import Slider

from read_file_data import get_csv_data
from packs_objects import get_packs
from objects import ObjectClass

sensor_display_time = 5.0

use_display_time = True
display_time_start = 600.0
display_time_end = 700.0

def draw():
    objects = get_csv_data('/work/fusion/as_main_module_sf/sensor_fusion3/cmake-build-release/data.csv')
    packs = get_packs(objects, use_display_time, display_time_start, display_time_end)

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

    pnts_measurements, = plt.plot([], [], "k1", mfc='none', alpha=0.01)
    pnts_candidate, = plt.plot([], [], "bv", mfc='none', alpha=0.1)
    pnts_global, = plt.plot([], [], "rp", mfc='none', alpha=0.3)

    axSlider = plt.axes([0.1, 0.2, 0.8, 0.05])
    sldr = Slider(ax=axSlider,
                  label="Time, sec",
                  valmin=packs[0].timestamp,
                  valmax=packs[-1].timestamp,
                  valstep=0.1,
                  color="green")

    ann_list = []

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

        pnts_m_x = [] #points measurements Ox
        pnts_m_y = [] #points measurements Oy
        pnts_c_x = [] #points candidate Ox
        pnts_c_y = [] #points candidate Oy
        pnts_g_x = [] #points global Ox
        pnts_g_y = [] #points global Oy

        for history_pack in new_history_packs:
            for obj_plot in history_pack.objects:
                if (obj_plot.is_global):
                    pnts_g_x.append(obj_plot.y)
                    pnts_g_y.append(obj_plot.x)
                elif (obj_plot.id != -1):
                    pnts_c_x.append(obj_plot.y)
                    pnts_c_y.append(obj_plot.x)
                else:
                    pnts_m_x.append(obj_plot.y)
                    pnts_m_y.append(obj_plot.x)


        pnts_measurements.set_data(pnts_m_x, pnts_m_y)
        pnts_candidate.set_data(pnts_c_x, pnts_c_y)
        pnts_global.set_data(pnts_g_x, pnts_g_y)

        for i, a in enumerate(ann_list):
            a.remove()
        ann_list[:] = []

        main_ids = []
        for history_pack in reversed(new_history_packs):
            for obj_plot in reversed(history_pack.objects):
                if (obj_plot.is_global and obj_plot.id not in main_ids):
                    ch_cntr = " "
                    for i in range(0, (len(obj_plot.channel_cntr)), 2):
                        ch_cntr += obj_plot.channel_cntr[i][0:3] + ":" + obj_plot.channel_cntr[i+1] + ";"
                    ann = ax.annotate(str(obj_plot.id) + "\n" + (ObjectClass.get(obj_plot.id_class)) + ch_cntr, (obj_plot.y, obj_plot.x), xytext =(obj_plot.y -3, obj_plot.x + 2), color = "black", fontsize = 6)
                    main_ids.append(obj_plot.id)
                    ann_list.append(ann)

        plt.draw()


    sldr.on_changed(update_data)
    plt.show()

def filter_history(ids, history):
    new_history = copy.deepcopy(history)
    for pack in new_history:
        i = 0
        del_index = []
        for obj in pack.objects:
            if (obj.id not in ids) and (obj.is_measurement == False):
                del_index.append(i)
            elif obj.is_measurement and new_history[-1].timestamp - obj.time >= sensor_display_time:
                del_index.append(i)

            i += 1

        for j in range(len(del_index), 0, -1):
            pack.objects.pop(j - 1)

    return new_history

if __name__== "__main__":
  draw()

