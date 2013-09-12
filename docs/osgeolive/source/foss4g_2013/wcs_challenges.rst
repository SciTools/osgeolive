=================
Challenges of WCS
=================

The OGC Web Coverage Service (WCS) defines a standard for requesting and transporting 'raw' coverage data [#f1]_. There is potential for WCS to be used for big data with file formats like CF-NetCDF being supported by the standard.

Operations:

.. image:: images/WCS_operations.png
    :width: 200px
    :align: center

.. todo::

   Iris builds on the semantics and data model from the Climate and Forecasting conventions for NetCDF (CF-NetCDF) which exist to define the metadata within NetCDF files in order to provide a definitive description of each of the data variables including their spatial and temporal properties. This enables users of data from different sources to decide which quantities are comparable and to build applications with powerful extraction, regridding, and display capabilities [1]. In this workshop we will introduce this new open source library, along with interesting multi-dimensional datasets, and show how "big data" can be served up using your existing open source software stack using GDAL, QGIS, GeoServer and OpenLayers. We will then investigate the challenges of OGC WCS 2.0 looking into the core functionality, such as subsetting, that all WCS implementations must provide when accessing coverages[2]. The ability to provide data sets of three, four, and higher-dimensions represents a significant expansion of the capabilities of web coverage services. We will demonstrate how the CF conventions cater for multidimensional data, and how Iris can provide a managing interface to provide NetCDF datasets. We will investigate the opportunities and challenges of using NetCDF as a transport mechanism and consider how current server technologies will be able to deliver the breath of WCS 2.0 services.

.. rubric:: Footnotes

.. [#f1] http://www.ogcnetwork.net/wcs
.. [#f2] http://cf-pcmdi.llnl.gov
