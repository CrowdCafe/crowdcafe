#!/bin/bash
# create settings_local.py
# create settings_sensitive.py

sudo virtualenv /opt/crowdcafe-local/
source /opt/crowdcafe-local/bin/activate
sudo python ez_setup.py
# for MAC install xcode and command line tools
# xcode-select --install
# open another terminal window, open virtualenv and continue
# sudo pip install http://effbot.org/media/downloads/Imaging-1.1.7.tar.gz
sudo pip install -r requirements.txt

python manage.py bower_install -- --allow-root
python manage.py syncdb
python manage.py runserver