import iris
import iris.coord_categorisation
import iris.quickplot as qplt
import matplotlib.pyplot as plt


def plot_surface_temp(fnme, year=2007, month='January'):
    """
    Plot mean surface temperature of a specified month, specified year
    and the difference between them.

    """
    cube = iris.load_cube(fnme, 'surface_temperature')
    # Convert temperature to degrees celsius
    cube.convert_units('degC')

    # Create categorisation coordinates
    iris.coord_categorisation.add_year(cube, 'time', name='year')

    # Extract a specified year of data
    specified_year = iris.Constraint(year=year)
    year_slice_cube = cube.extract(specified_year)

    # Determining year average surface temperature
    year_average = year_slice_cube.collapsed('year', iris.analysis.MEAN)

    iris.coord_categorisation.add_month_fullname(year_slice_cube, 'time',
                                                 name='month')

    # Extract a specified month of a specified year of data
    specified_month = iris.Constraint(month=month)
    month_slice_cube = year_slice_cube.extract(specified_month)

    difference_cube = year_average - month_slice_cube
    difference_cube.long_name = (
        'Difference between mean \ntemperature of '
        '{} and {}'.format(month, year))

    # Plot
    plt.figure(figsize=(20, 5))
    plt.subplot(131)
    qplt.contourf(year_average)
    ax = plt.gca()
    ax.coastlines()
    ax.set_title('Mean temp of {}'.format(year))

    plt.subplot(132)
    qplt.contourf(month_slice_cube)
    ax = plt.gca()
    ax.coastlines()
    ax.set_title('Mean temperature of {} {}'.format(month, year))

    plt.subplot(133)
    qplt.contourf(difference_cube)
    plt.gca().coastlines()

    plt.show()


if __name__ == '__main__':
    plot_surface_temp('ostia_monthly_complete.nc')
