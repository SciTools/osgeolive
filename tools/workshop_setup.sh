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
# This version of the workshop_setup script also calls a modified version
# of install_iris.sh to update both Iris and Cartopy, and also fixes a bug
# that exists on OSGeo Live 7.0 with NetCDF4 support.

#Settings for University of Nottingham
echo 'export http_proxy="http://128.243.253.109:8080"' >> /etc/environment
echo 'export http_proxy="http://128.243.253.109:8080"' >> /etc/bash.bashrc

wget https://raw.github.com/SciTools/osgeolive/master/tools/install_iris2.sh
sudo bash ./install_iris2.sh 
rm ./install_iris2.sh

# Install git
apt-get install -y git
 
echo "Downloading and build workshop material"
mkdir -p ~/git
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
# Also link sample_data to default location
ln -s ~/git/iris-sample-data/sample_data /usr/local/lib/python2.7/dist-packages/Iris-1.5.0-py2.7-linux-i686.egg/iris/sample_data

# Fix up Iris site.cfg so that location of sample data is known
echo """[System]
udunits2_path = /usr/lib/i386-linux-gnu/libudunits2.so
 
[Resources]
sample_data_repository = /home/user/git/iris-sample-data/sample_data
""" > /usr/local/lib/python2.7/dist-packages/Iris-1.4.0-py2.7-linux-i686.egg/iris/etc/site.cfg
 
echo "Setting keyboard to UK now, and for next boot"
echo "setxkbmap gb" >> ~/.bashrc
setxkbmap gb
 
echo "Enable auto-complete in the python interpreter"
echo """
import rlcompleter, readline
readline.parse_and_bind('tab:complete')
""" > ~/.pythonrc
echo "export PYTHONSTARTUP=~/.pythonrc" >> ~/.bashrc
export PYTHONSTARTUP=~/.pythonrc
 
echo "Get World shapefile data for testing"
mkdir -p ~/iris_workshop/data/qgis/
#cd ~/iris_workshop/data/qgis/
#wget http://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip
#unzip TM_WORLD_BORDERS-0.3.zip
cd ~
 
echo "Linking OSGeo Live NetCDF sample data"
ln -s ~/data/netcdf ~/iris_workshop/data/netcdf

sudo chown -R user: git iris_workshop

# Note: installing and building PySide dependancy is slow
#wget https://raw.github.com/SciTools/osgeolive/master/tools/install_cubeviz.sh
#sudo bash ./install_cubeviz.sh 
#rm ./install_cubeviz.sh
wget https://gist.github.com/iedwards/6578183/raw/f64d5620bf32a4eb5cd11bcbd526de7d3e9aa5c3/usethisone
