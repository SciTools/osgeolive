#!/usr/bin/env bash
#
# Please execute this script using:
# sudo bash ./workshop_setup.sh
#
# Although this script is located in the SciTools/osgeolive repository, it is
# intended that the script will be downloaded independently.
# Execution of the script will then download (clone) the osgeolive repository
# as well as other data that is needed for the workshop.
#
# This version of the workshop_setup script also fixes a bug on OSGeo Live 7.0
 
 
# Install git
apt-get install -y git
 
# Replace the build and dev packages that were removed to keep the Live ISO small
apt-get install -y python-dev libhdf5-serial-dev libnetcdf-dev \
libgeos-dev libproj-dev \
libjasper-dev libfreetype6-dev libpng-dev tk-dev
 
echo "Fixing NetCDF4 support on OSGeo Live 7.0 (pip was broken at time of freeze)"
pip install -I netCDF4==1.0.4
 
echo "Allow MatplotLib to default to the most recent (was locked to 1.2.0 in Live 7.0)"
easy_install -U distribute
pip install matplotlib --upgrade
 
# Replace the Cartopy data and examples that were also removed
mkdir -p ~/git
cd ~/git
git clone https://github.com/SciTools/cartopy.git
mv cartopy/lib/cartopy/data /usr/local/lib/python2.7/dist-packages/cartopy/data
mv cartopy/lib/cartopy/examples /usr/local/lib/python2.7/dist-packages/cartopy/examples
rm -rf ~/git/cartopy
 
echo "Downloading and build workshop material"
cd ~/git
git clone https://github.com/SciTools/osgeolive.git
cd ~/git/osgeolive/docs/osgeolive
make html
 
echo "Create workshop folder"
mkdir -p ~/iris_workshop
ln -s ~/git/osgeolive/docs/osgeolive/build/html ~/iris_workshop/docs
 
# Download Iris sample data
cd ~/git
git clone http://github.com/SciTools/iris-sample-data.git
mkdir -p ~/iris_workshop/data
ln -s ~/git/iris-sample-data/sample_data ~/iris_workshop/data/sample_data
 
# Fix up Iris site.cfg so that location of sample data is know
echo """[System]
udunits2_path = /usr/lib/i386-linux-gnu/libudunits2.so
 
[Resources]
sample_data_repository = /home/user/git/iris-sample-data/sample_data
""" > /usr/local/lib/python2.7/dist-packages/Iris-1.4.0-py2.7-linux-i686.egg/iris/etc/site.cfg
 
echo "Setting keyboard to UK now, and for next boot"
echo "setxkbmap gb" >> ~/bash.rc
setxkbmap gb
 
echo "Enable auto-complete in the python interpreter"
echo """
import rlcompleter, readline
readline.parse_and_bind('tab:complete')
""" > ~/.pythonrc
echo "export PYTHONSTARTUP=~/.pythonrc" >> ~/.bashrc
 
 
echo "Get World shapefile data for testing"
mkdir -p ~/iris_workshop/data/qgis/
cd ~/iris_workshop/data/qgis/
wget http://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip
unzip TM_WORLD_BORDERS-0.3.zip
cd ~
 
echo "Linking OSGeo Live NetCDF sample data"
ln -s ~/data/netcdf ~/iris_workshop/data/netcdf

sudo chown -R user: git iris_workshop
 
echo "Launch the Iris workshop introduction now (and on future boot)"
echo "firefox ~/iris_workshop/docs/index.html &" >> .bashrc
firefox ~/iris_workshop/docs/index.html &
