sudo apt-get -y install python2.7-dev
sudo apt-get -y install qt-sdk
sudo apt-get -y --force-yes install cmake
sudo apt-get -y git
 
# the following two lines may not be necessary
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
sudo python ez_setup.py
 
mkdir -p ~/git
cd ~/git
git clone https://github.com/PySide/pyside-setup.git pyside-setup
cd pyside-setup
python2.7 setup.py bdist_egg --version=1.2.1
 
sudo easy_install-2.7 dist/PySide-1.2.1-py2.7.egg
sudo python2.7 pyside_postinstall.py -install
cd ~

echo """#!/usr/bin/env bash
export PYTHONPATH='${PYTHONPATH}:/home/user/git/thea/lib'
python /home/user/git/thea/lib/thea/main.py &
""" > ~/cubeviz
chmod a+x ~/cubeviz

