#!/usr/bin/env bash

sudo python get-pip.py

sudo wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux32.tar.gz
sudo tar -xzf geckodriver-v0.18.0-linux32.tar.gz
sudo mv geckodriver /usr/local/bin/

#sudo apt-get install -y nodejs
#sudo apt-get install -y npm
#npm install phantomjs-prebuilt

pip install virtualenv

virtualenv venv

. venv/bin/activate
pip install -r reqs

# venv/bin/python scrap.py