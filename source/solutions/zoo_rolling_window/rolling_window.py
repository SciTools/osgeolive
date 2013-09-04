import base64
import cStringIO
import sys

import iris
import iris.plot as iplt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


AGGREGATORS = {'mean': iris.analysis.MEAN, 'max': iris.analysis.MAX}


def rolling_window(lat, lon, period, aggregator):
    #a1b = iris.load_cube(iris.sample_data_path('A1B_north_america.nc'))
    a1b = iris.load_cube('/home/user/git/osgeolive/source/solutions/zoo_rolling_window/A1B_north_america.nc')
    location = [('latitude', lat), ('longitude', lon)]
    time_series = iris.analysis.interpolate.linear(a1b, location)
    time_series.coord('time').bounds = None
    time_series_windowed = time_series.rolling_window(
        'time', aggregator, period)

    plt.figure(figsize=(3, 2))
    iplt.plot(time_series, color='0.7', label='no filter')
    iplt.plot(time_series_windowed, color='b',
              label='{}-year filter'.format(period))
    title = 'HadGEM2 A1B-Image Scenario\nLat: {}, lon: {}'
    #plt.title(title.format(lat, lon))
    #plt.xlabel('Time')
    #plt.ylabel('Air temperature / K')
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(50))
    plt.gca().format_xdata = mdates.DateFormatter('%Y')
    #plt.legend()


def RollingWindow(config, inputs, outputs):
    plt.switch_backend('agg')
    lat = float(inputs['lat']['value'])
    lon = float(inputs['lon']['value'])
    aggregate = inputs['agg']['value']
    method, period = aggregate.split('_')
    aggregator = AGGREGATORS[method]
    period = int(period)

    rolling_window(lat, lon, period, aggregator)

    img_data = cStringIO.StringIO()
    plt.savefig(img_data, format='png')
    outputs['Result']['value'] = img_data.getvalue()

    return 3 # i.e. zoo.SERVICE_SUCCEEDED


if __name__ == '__main__':
    rolling_window(36, -107, 30, iris.analysis.MEAN)
    #rolling_window(36, -107, 30, iris.analysis.MAX)
    plt.show()
