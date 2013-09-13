============================
Publishing data to GeoServer
============================

This example publishes an Iris cube to geoserver, then plots the new WMS.


Geoserver
---------
You can start GeoServer from the Xubuntu desktop by navigating to:

	Geospatial > Web Services > GeoServer > Start GeoServer

This tutorial controlls GeoServer programatically
but there is also a web interface available here:

	http://localhost:8082/geoserver/web/
 

Load some data
--------------
Let's load some global temperature data from a PP file.
This will give us a 2D horizontal "cube".

.. code-block:: python

    import iris
    
    filename = iris.sample_data_path("A1B.2098.pp")
    cube = iris.load_cube(filename)


Convert to GeoTIFF
------------------
2D horizontal cubes can be exported as GeoTIFF files.
We'll need to add "bounds" to our latlon coordinates first.

.. code-block:: python

    import iris.experimental.raster

    cube.coord(axis="x").guess_bounds()
    cube.coord(axis="y").guess_bounds()
    iris.experimental.raster.export_geotiff(cube, 'temp.geotiff')


Publish to GeoServer
--------------------
Using our little helper functions in geopub.py, 
we can connect to geoserver and create a "Coverage Store" for raster data.

.. code-block:: python

    from geopub import *

    server = "localhost:8082"
    workspace = "iris_test_ws"
    coveragestore = "iris_test_cs"
    filename = "file.geotiff"

    connect_to_server(server, 'admin', 'geoserver')
    create_workspace(server, workspace)  # fail if exist
    create_coveragestore(server, workspace, coveragestore)   # fail if exist
    data = open('temp.geotiff', "rb").read()
    upload_file(server, workspace, coveragestore, filename, data)

GeoServer creates a "coverage" object and a "layer" for us too.


Tweaking coverage
-----------------
If GeoServer doesn't get correct geographic information, we can correct it.

.. code-block:: python

    data = '<coverage>'\
                '<srs>EPSG:4326</srs>'\
                '<nativeCRS>EPSG:4326</nativeCRS>'\
                ' <nativeBoundingBox>'\
                    '<minx>-180.0</minx>'\
                    '<maxx>180.0</maxx>'\
                    '<miny>-90.0</miny>'\
                    '<maxy>90.0</maxy>'\
                    '<crs>EPSG:4326</crs>'\
                '</nativeBoundingBox>'\
                '<enabled>true</enabled>'\
            '</coverage>'
    update_coverage(server, workspace, coveragestore, coveragestore, data)


Access via WMS
--------------
Let's use our new service!
We'll setup a cartographic plot using matplotlib and cartopy,
then request a background jpeg from our new WMS.

.. code-block:: python

    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt

    wms_server = '{server}/{workspace}/wms?service=WMS'.format(server=server, workspace=workspace)
    layers = '{workspace}:{coveragestore}'.format(workspace=workspace, coveragestore=coveragestore)

    plt.axes(projection=ccrs.PlateCarree())
    plt.gca().set_extent([-40, 40, 20, 80])
    wms_image(wms_server, layers)
    plt.gca().coastlines()
    plt.show()

