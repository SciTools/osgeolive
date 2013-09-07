import os

import matplotlib.pyplot as plt

import iris
from iris.experimental.animate import animate
import iris.plot as iplt


def custom_contour(*args, **kwargs):
    result = iplt.contour(*args, colors='white')
    plt.clabel(result, inline=1, fontsize=14, fmt='%i', colors='white')
    ax = plt.gca()
    ax.stock_img()
    ax.coastlines(resolution='50m')


def main(path):
    fdirs = os.path.join(path, 'pressure/*')

    pressure = iris.load_cube(fdirs, 'mslpressure')

    pressure_slices = pressure.slices(['projection_y_coordinate',
                                       'projection_x_coordinate'])
    # Subsample the cube, correct units and convert to millibars
    pressure_slices = [slice[::10, ::10] for slice in pressure_slices]
    for slice in pressure_slices:
        slice.units = 'mb/10'
        slice.convert_units('mb')

    ani = animate(pressure_slices, custom_contour)

    print 'saving...'
    ani.save('wind_simple.avi', bitrate=1000)
    print 'completed'
    plt.show()


if __name__ == '__main__':
    main('/data/local/cpelley/tmp_data/FOSS4G')
