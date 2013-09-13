=============
WPS with Iris
=============

Overview
--------

This example builds on the previous scenarios which worked with Iris,
OpenLayers, and WPS, to build an interactive web map which allows the
end user to click on any location to view a dynamically processed,
time-series graph for that location.

To enable this interface, you will build a WPS service which returns a
time-series graph for a given latitude/longitude point. The user of the
service will also specify a rolling-window operation to apply along the
time axis of the data before it is plotted. For example, the user might
choose to apply a 30-year rolling mean, or a 5-year rolling maximum.

This example will use a global time-series dataset that is bundled with
OSGeo-Live. You can find the dataset in:

    /usr/local/share/data/netcdf/txxETCCDI_yr_MIROC5_historical_r2i1p1_1850-2012.nc

Describing the service
----------------------

In the previous section you saw how each input to your WPS service is
described by a corresponding section in the `.zcfg` file. For example:

.. code-block:: none

  [lat]
   Title = Latitude of sample point
   Abstract = Latitude of sample point.
   minOccurs = 1
   maxOccurs = 1
   <LiteralData>
       dataType = float
       <Default />
   </LiteralData>

So for this example you will need a section like this for each of the
latitude, longitude, period, and aggregation parameters. Take care to
ensure the correct data type for each parameter.

Unlike the previous example, the output of your graph service will need
to be an image, and not just simple textual/numeric data. WPS deals with
this kind of data by allowing the service description to include a MIME
type for the value. In this case you will want to use the MIME type for
an image format supported by matplotlib, such as `image/png`.

To specify a MIME type you will need to use a `<ComplexData>` section
instead of the `<LiteralData>` section used previously.

.. code-block:: none

   <ComplexData>
     <Default>
       mimeType = image/png
       encoding = base64
     </Default>
   </ComplexData>

Note the inclusion of an `encoding` attribute which tells ZOO how to
encode the image data within an XML response.

Your final configuration file should look something like
:doc:`this <wps_with_iris/configuration>`.

As in the previous example, you can check that ZOO has been able to read
your configuration file by making a `DescribeProcess` request:

    http://localhost/cgi-bin/zoo_loader.cgi?request=DescribeProcess&service=WPS&version=1.0.0&Identifier=RollingWindow


Building the engine
-------------------

It's a good idea to separate the "core" of your implementation from the
ZOO-specific handling of inputs and outputs. This allows you to re-use
the core implementation in other contexts (e.g. a command-line tool),
and it makes it easier and quicker to test. So for this example you will
want to write a function which accepts latitude, longitude, period, and
aggregation, and which sets up a matplotlib plot (but does not show it).

For example:

.. code-block:: python

    import matplotlib.pyplot as plt

    def do_the_good_stuff(lat, lon, period, aggregation):
        ...

        plt.plot(...)

Within this function you need to:
 * Load the source data.
 * Choose the time series relevant to the given location.
   You might like to use the `iris.analysis.interpolate.linear()
   <http://scitools.org.uk/iris/docs/latest/iris/iris/analysis/interpolate.html#iris.analysis.interpolate.linear>`_ function here.
 * Calculate the `rolling_window()
   <http://scitools.org.uk/iris/docs/latest/iris/iris/cube.html#iris.cube.Cube.rolling_window>`_
   using the given period and aggregation.
 * Plot the rolling window data (and possibly the raw time series for
   comparison).

NB. The default matplotlib behaviour will probably give you far too many
tick marks along the date axis of your plot. As a result they all merge
together to make an unreadable mess. The following code snippet lets you
control how often you want ticks to sort this out:

.. code-block:: python

    import matplotlib.dates as mdates

    plt.gca().xaxis.set_major_locator(mdates.YearLocator(50))

Now that you have your core function, you might like to add the ability
to test your function from the command line. Using the standard Python
idom you will need something like:

.. code-block:: python

    if __name__ == '__main__':
        rolling_window(36, -107, 30, iris.analysis.MEAN)
        plt.show()

Now you can execute `python rolling_window.py` and check the results.

With the core function in-place and working, it's time to provide the
ZOO-specific wrapper. As with the previous example, this needs a Python
function that takes three arguments: `config, inputs, outputs`. And it's
the job of this function to:

 * Validate and interpret incoming values.
 * Call your core function.
 * Return the plot as a the bytes for a PNG.

To deal with the incoming values, you will need to extract the `"value"`
key from each of your inputs and convert it to the form needed by your
core function. Unfortunately, ZOO does not automatically provide inputs
declared as `"float"` as Python floats, but the following snippet does
the job:

.. code-block:: python

   lat = float(inputs(['lat']['value'])

Having parsed you input values and called your core function, you now
need to render your plot as a PNG and place the resulting bytes in
`outputs['Result']['value']`. (NB. ZOO will take care of base64 encoding
the bytes in the result value.) In versions of Python 2.7 and above you
can use the `io.BytesIO()` class in conjunction with matplotlib's
`plt.savefig()` function to do this as follows:

.. code-block:: python

    import io

    # ... set up your plot ...

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    outputs['Result']['value'] = img_data.getvalue()

Having put all this together, your Python code should look something
like :doc:`this <wps_with_iris/implementation>`.

To test your new service, encode sample values for all four parameters
into a single request, such as:

   http://localhost/cgi-bin/zoo_loader.cgi?request=Execute&service=WPS&version=1.0.0&Identifier=Hello&DataInputs=lat=52.95;lon=1.1333;period=3;agg=mean

As for the previous example, this will return an XML document which
contains the output of your function embedded within it. But in this
case the output of your function is a lot of bytes which have been
base64 encoded by ZOO, so it will just look like a seemingly random
sequence of numbers, letters, and punctuation. What you really want is
to view the PNG as an actual image. For this you need to append
`&RawDataOutput=Result`.

   http://localhost/cgi-bin/zoo_loader.cgi?request=Execute&service=WPS&version=1.0.0&Identifier=Hello&DataInputs=lat=52.95;lon=1.1333;period=3;agg=mean&RawDataOutput=Result

Congratulations! You are now the proud owner of a WPS service which
works with real data, performs real statistical analyses, and returns
easy to read graphs.


Putting it all together
-----------------------

Now that you have a working WPS graphing service, the final piece of
the puzzle is to provide a web page containing:

 * An OpenLayers map (as discussed in a previous example).
 * HTML controls to specify the period and aggregation for the graph.
 * JavaScript to request graph images from your service.

You may wish to provide the period and aggregation options via HTML
`SELECT` controls for simplicity.

To obtain the latitude and longitude when the user clicks the map you
can register a `"click"` handler which uses the `getLonLatFromPixel()`
method on your OpenLayers map. For example:

.. code-block:: javascript

    map.events.register("click", map, function(e) {
        position = map.getLonLatFromPixel(e.xy);

        // Call your WPS service with position.lat, position.lon
        // and the period and aggregation choices.

    });

The OpenLayers JavaScript API does provide some support for making WPS
requests but sadly, at the time of writing, it does not support
requesting the raw data needed to obtain a PNG. Instead, you can
construct the URL "by hand" and substitute the parameter values:

.. code-block:: javascript

    wps_url = 'http://localhost/cgi-bin/zoo_loader.cgi?request=Execute&service=WPS&version=1.0.0&Identifier=RollingWindow&DataInputs=lat=' + position.lat + ';lon=' + position.lon + ';agg=' + agg + ';period=' + period + '&RawDataOutput=Result@mimeType=image/png';

Your final web page code might look something like
:doc:`this <wps_with_iris/web_page>`. (NB. This page contains additional
JavaScript to use an OpenLayers pop-up, and automatically update the
graph when the user chooses a new value for either SELECT control.)
