=================
What is Big Data?
=================

There is currenly no commonly accepted definition of "big data", but data receiving this label tends to have a combination of the following characteristics [#f1]_:

- Volume - Large amount of data are stored and analysed
- Variety - Multiple types of data - possibly from multiple sources
- Velocity - Data produced at high rates
- Value - Data with measurable benefit
- Veracity - Assessing the correctness of data

Types of big data
-----------------

In this workshop we will explore large multi-dimensional datasets such as those found in the fields of weather and climate science, and also introduce data models and tools designed specifically to work with these data.

Note that we'll be working with dense, gridded big data that is usual dense and numeric. In contrast, other types of big data may be very sparse, or may consist of large volumes of text or other data amalgamated from different sources.

The top level object that we will work with in this workshop is called a cube. A cube contains data and metadata about a phenomenon. A cube is an interpretation of the *Climate and Forecast (CF) Metadata Conventions* whose purpose is to:

    *require conforming datasets to contain sufficient metadata that they are self-describing... including physical 
    units if appropriate, and that each value can be located in space (relative to earth-based coordinates) and time.*

Below is a pictorial example of a cube containing a single phenomena (Air Temperature), along with latitude, longitude and height coordinates:

.. image:: images/multi_array_to_cube.png


.. rubric:: Footnotes

.. [#f1] Categories of big data taken from the Autumn 2013 edition of *IT Now* from the British Computer Society: http://itnow.oxfordjournals.org/content/55/3.toc
