sudo apt-get install python-software-properties
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs

apt-get install npm
npm config set registry http://registry.npmjs.org/
npm install -g bower

gunicorn_django --workers=1 --bind 5.101.96.187:80