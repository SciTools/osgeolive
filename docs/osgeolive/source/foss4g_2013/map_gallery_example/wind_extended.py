import os

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
import iris
import iris.plot as iplt


def quiver_plot(wind_slice, direction_slice, step):
    """
    Calculate U and V and plot quivers.

    """
    U = (wind_slice.data) * np.cos(np.deg2rad(direction_slice.data))
    V = (wind_slice.data) * np.sin(np.deg2rad(direction_slice.data))
    X = wind_slice.coord('projection_x_coordinate').points
    Y = wind_slice.coord('projection_y_coordinate').points

    arrows = plt.quiver(X[::step], Y[::step],
                        U[::step, ::step], V[::step, ::step],
                        units='xy',
                        headwidth=2,
                        transform=ccrs.OSGB(), zorder=1.0)
    return arrows


def animation_plot(i, pressure, wind, direction, step=24):
    """
    Function to update the animation frame.

    """
    # Clear figure to refresh colorbar
    plt.gcf().clf()

    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_extent([-10.5, 3.8, 48.3, 60.5], crs=ccrs.Geodetic())

    contour_wind = iplt.contourf(wind[i][::10, ::10], cmap='YlGnBu',
                                 levels=range(0, 31, 5))
    contour_press = iplt.contour(pressure[i][::10, ::10], colors='white',
                                 linewidth=1.25, levels=range(938, 1064, 4))
    plt.clabel(contour_press, inline=1, fontsize=14, fmt='%i', colors='white')
    quiver_plot(wind[i], direction[i], step)
    plt.gca().coastlines(resolution='50m')

    time_points = pressure[i].coord('time').points
    time = str(pressure[i].coord('time').units.num2date(time_points)[0])
    plt.gca().set_title(time)

    colorbar = plt.colorbar(contour_wind)
    colorbar.ax.set_ylabel('Wind speed ({})'.format(str(wind[i].units)))


def main(fdir):
    fdirs = [os.path.join(fdir, path) for path in ['pressure/*', 'wind/*']]

    pressure, direction, wind = iris.load_cubes(
        fdirs, ['mslpressure', 'Direction', 'Windspeed'])

    # Turn these generators into lists, so that the animation can be repeated
    pressure_slices = list(pressure.slices(['projection_y_coordinate',
                                            'projection_x_coordinate']))
    # Correct pressure units and convert to millibars.
    for slice in pressure_slices:
        slice.units = 'mb/10'
        slice.convert_units('mb')

    direction_slices = list(direction.slices(['projection_y_coordinate',
                                              'projection_x_coordinate']))

    wind_slices = list(wind.slices(['projection_y_coordinate',
                                    'projection_x_coordinate']))
    # Correct wind speed units and convert to m/s.
    for slice in wind_slices:
        slice.units = 'knot/10'
        slice.convert_units('m/s')

    frames = xrange(len(pressure_slices))
    fig = plt.gcf()
    ani = animation.FuncAnimation(fig, animation_plot,
                                  frames=frames,
                                  fargs=(pressure_slices, wind_slices,
                                         direction_slices),
                                  interval=200)
    print 'saving...'
    ani.save('wind.avi', bitrate=5000)
    print 'completed'
    plt.show()


if __name__ == '__main__':
    main('data/map_gallery')
