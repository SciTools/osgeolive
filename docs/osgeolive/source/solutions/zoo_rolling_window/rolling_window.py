import io
import os.path
import sys

import iris
import iris.plot as iplt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


AGGREGATORS = {'mean': iris.analysis.MEAN, 'max': iris.analysis.MAX,
               'min': iris.analysis.MIN}


DATA_DIR = '/usr/local/share/data/netcdf'
DATA_FILE = 'txxETCCDI_yr_MIROC5_historical_r2i1p1_1850-2012.nc'


def rolling_window(lat, lon, period, aggregator):
    src_data = iris.load_cube(os.path.join(DATA_DIR, DATA_FILE))
    location = [('latitude', lat), ('longitude', lon)]
    time_series = iris.analysis.interpolate.linear(src_data, location)

    # Get rid of the time bounds to suppress the warning from
    #`rolling_window()`.
    time_series.coord('time').bounds = None

    time_series_windowed = time_series.rolling_window('time', aggregator,
                                                      period)

    plt.figure(figsize=(3, 2))
    iplt.plot(time_series, color='0.7', label='no filter')
    iplt.plot(time_series_windowed, color='b',
              label='{}-year filter'.format(period))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(50))


def RollingWindow(config, inputs, outputs):
    # Ensure matplotlib is using a non-GUI "backend" to do its drawing.
    plt.switch_backend('agg')

    # Parse and sanity check the incoming values.
    # NB. You must never trust values which come from an external
    # source.
    lat = float(inputs['lat']['value'])
    lon = float(inputs['lon']['value'])
    aggregate = inputs['agg']['value']
    period = int(inputs['period']['value'])
    aggregator = AGGREGATORS[aggregate]

    rolling_window(lat, lon, period, aggregator)

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    # NB. ZOO will take care of the base64 encoding, so we just return
    # the raw bytes.
    outputs['Result']['value'] = img_data.getvalue()

    return 3  # i.e. zoo.SERVICE_SUCCEEDED


# This allows our plot to be tested from the command line.
if __name__ == '__main__':
    rolling_window(36, -107, 30, iris.analysis.MEAN)
    plt.show()
