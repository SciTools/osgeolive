import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
import iris
import iris.analysis.cartography
import iris.coord_systems


def plot_hadgem(x, y, d, proj, **kwargs):
    """
    Function for plotting the hadgem data.

    Args:

        * x (array-like object):
            Plotting x coordinate
        * y (array-like object):
            Plotting y coordinate
        * d (array-like object):
            Data
        * proj (:class:`~cartopy.crs.Projection`):
            Chosen projection for the resulting plot.

    See :class:`matplotlib.pyplot.pcolormesh` for details of valid keyword
    arguments.

    """
    ax = plt.axes(projection=proj)
    plt.pcolormesh(x, y, d, **kwargs)
    plt.colorbar(orientation='horizontal')
    ax.coastlines()
    ax.gridlines()
    plt.show()


def resample_plot(nx=1000, ny=1000, proj=ccrs.PlateCarree()):
    """
    Resample the hadgem data and plot it.

    Kwargs:

        * nx (int, float or long):
            Desired number of sample points in the x direction.
        * ny (int, float or long):
            Desired number of sample points in the y direction.
        * target_proj (:class:`~cartopy.crs.Projection` or \
        :class:`iris.coord_systems.CoordSystem` instance)
            Determines the projection of the plotted data.
  
    Returns:
        :class:`iris.cube.Cube` of, re-gridded using nearest neighbour onto a
        :class:`~iris.coord_systems.GeogCS`.

    """

    # Pick first time slice (1 of 1)
    fnme = '/data/local/dataZoo/NetCDF/orca0.25/hf_xexoc.nc'
    cube = iris.load_cube(fnme)[0]

    # Extend the mask over extremes of the data
    mask_values = np.ma.masked_greater(cube.data, 1.5e4)
    cube.data.mask = np.ma.mask_or(cube.data.mask, mask_values.mask)

    # Re-sample our data (nn re-gridding)
    target_crs = iris.coord_systems.GeogCS(semi_major_axis=6378137.0,
                                           inverse_flattening=298.257223563)
    # Re-sample our data (nn re-gridding) to our specified projection
    resampled, extent = iris.analysis.cartography.project(cube, target_crs,
                                                          nx=nx, ny=ny)

    target_proj = proj
    new_cube, extent = iris.analysis.cartography.project(cube, target_proj,
                                                         nx=nx, ny=ny)

    x = new_cube.coord('projection_x_coordinate').points
    y = new_cube.coord('projection_y_coordinate').points
    d = new_cube.data

    # Plot projected data
    plot_hadgem(x, y, d, proj=proj)

    return resampled


if __name__ == '__main__':
    cube = resample_plot(nx=1000, ny=1000, proj=ccrs.SouthPolarStereo())
    iris.save(cube, 'hadgem_resampled.nc')
