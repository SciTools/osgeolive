=============
WPS with Iris
=============

.. todo::

   Description of the A1B.2098.pp dataset (or alternative if substituded)

This example builds on the A1B.2098 scenario that we worked with in QGIS. Instead of asking the user to open the dataset in Iris and write out a part of it as a GeoTiff we will instead call Iris directly from the web and ask for a specific value from the dataset.

**Data:** ~/iris_workshop/data/sample_data/A1B.2098.pp

**Remit:** Given the sample data above, create a ZOO Service that returns a temperature value (in the specified units :math:`^{\circ}K,^{\circ}C` or :math:`^{\circ}F`) for a given latitude and longitude.

**Example solution:**

.. code-block:: python

   import iris
   cube = iris.load_cube('A1B.2098.pp')
   print cube
   # return temperature value (in specified units) given a lat/lon location

.. admonition:: Remember...

   After you're created your .zcfg and .py files, copy them into the same folder as zoo_loader.cgi, e.g.

   ``sudo cp hello_iris.zcfg /usr/lib/cgi-bin/``


Challenge
---------
Can you add to the ZOO web demo at http://localhost/zoo-demo/spatialtools.html to return values from the A1B.2098 data set?

.. Note::

   For the ZOO demo to function correctly, you must first start GeoServer

.. admonition:: Hints:

   To work with the existing demo:
   1. Click on one of the polygons for a state
   2. Select the Centroid button. Icons for all of the tools that can work with the centroid's latitude and longitude coordinate are displayed

