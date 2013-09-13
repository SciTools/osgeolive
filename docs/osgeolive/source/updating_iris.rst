===============================
Updating Iris on OSGeo Live 7.0
===============================

.. Note::

   If you are using OSGeo Live *Iris Workshop edition* (running from a USB memory stick) then your version of Iris is already up to date, and there is no need to follow these instructions. You can access the local workshop material via the "Iris Workshop" icon on the Desktop.

To update your version of Iris on OSGeo Live 7.0 follow the process below. Please note that these instructions are only intended for version 7.0 of OSGeo Live and may have undesired results if used on a different distribution.

Navigate to *Applications* > *Accessories* > *Terminal Emulator*, and enter the following commands:

.. code-block:: python

   wget https://raw.github.com/SciTools/osgeolive/master/tools/workshop_setup.sh
   wget https://raw.github.com/SciTools/osgeolive/master/tools/install_iris2.sh
   sudo bash ./workshop_setup.sh

This script makes a number of changes to your OSGeo Live setup, including:

- Fixing a bug with NetCDF4 support on OSGeo Live 7.0
- Updating Python's Matplotlib library to the latest version
- Replacing sample data that was removed to keep live disc small and portable
- Changing your keyboard layout to British (FOSS4G 2013 was in the UK)
- Enabling auto-complete in the Python interpreter
- Making some updates to your version of Iris

When the script has completed, an "Iris Workshop" icon will be added to the Desktop. Double-click this icon to start the FOSS4G 2013 workshop in Firefox.
