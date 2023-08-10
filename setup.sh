#!/usr/bin/env bash

echo "Running Setup Script for Pleasure Dairy."

# Install Python dependencies
if [[ "$(python3 -V)" =~ "Python 3" ]]
then
    echo "Verified Python 3 tk is already installed as default version"
else
    brew install python3
fi

if [[ "$(virtualenv --version)" =~ "virtualenv" ]]
then
    echo "Verified virtualenv is already installed"
else
    pip install virtualenv
fi

# Create virtualenv
if [ -d "./cbenv" ]
then
    echo "Virtualenv already exists"
else
    echo "Creating virtualenv"
    # TODO - verify works / tk call out is necessary
    virtualenv pdenv
fi

source pdenv/bin/activate

# Install Python dependencies
pip3 install --upgrade pip
pip3 install numpy
pip3 install matplotlib
pip3 install scipy

# Add packages to python path
current_path=$(pwd)  # for example $PWD or $(pwd)
package_path='/pleasure_dairy/'
newfilepath="$current_path"/"$( basename "$package_path" )"
pwd > pdenv/lib/python3.11/site-packages/cb.pth