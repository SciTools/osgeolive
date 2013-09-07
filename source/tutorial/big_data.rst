=====================
Working with Big Data
=====================

Visualisation
-------------


Animation
---------
This exercise is split into two: The first is the animation of pressure contours with time; The later is a more advanced custom animation, over-plotting various information.

Exercise 1
**********
.. image:: wind_simple.png
    :width: 600px
    :align: center

* Load all the specified data within a specified directory and we expect to return a single cube for this pressure data.
* Slice this cube to obtain an iterator of cubes, each one corresponding to a 2-dimensional slice at a specific time.
* Convert the units of each slice, and sub-sample the data for every 10 points in order to reduce the number of points being plotted.
* Define a custom plotting function to allow coastlines and a stock image to be plotted.
* Call the iris animate wrapper, providing it with both our data and custom plotting function.
* Save this animation to an avi (this can take some time).
* Plot this animation to the screen.

.. literalinclude:: wind_simple.py

Exercise 2
**********

.. image:: wind_extended.png
    :width: 600px
    :align: center

In this exercise, we contour the wind speed, contour the pressure data, calculate the 'u' and 'v' components of the wind and plot these as quivers.  This is again animated as slices across time.

* Construct the path to each set of data (pressure, windspeed, direction).
* Convert the units of pressure to millibars and wind speed to meters per second.
* Define a function which determines the horizontal and vertical component of the wind by utilising the direction and magnitude information and plots these vectors as quivers.
* Define a function which is called at each animation frame to plot (this will call our above quiver calculating/plotting function.

  * Define our axes with a Mercator projection and choose suitable limits based on a region of interest.
  * Contour the wind magnitude data (filled contour).
  * Contour the pressure (contour lines with labels indicating the pressure).
  * Call our quiver plotting function.
  * Add any additional information to the plot such as colorbars, titles which indicate the current time slice etc.

.. literalinclude:: wind_extended.py
