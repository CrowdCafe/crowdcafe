#!/bin/bash
# create settings_credentials.py https://gist.github.com/pavelk2/68dc3c62bf7a745b0e4e
# create settings_database.py https://gist.github.com/pavelk2/2638137e8d368b97412b

sudo virtualenv /opt/crowdcafe-local/
source /opt/crowdcafe-local/bin/activate
sudo python ez_setup.py
# for MAC install xcode and command line tools
# xcode-select --install
# open another terminal window, open virtualenv and continue
# sudo pip install http://effbot.org/media/downloads/Imaging-1.1.7.tar.gz
pip install -r requirements.txt

python manage.py bower_install -- --allow-root
python manage.py syncdb
python manage.py runserver