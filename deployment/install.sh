#! /bin/bash

apt install -y nginx python3 python3-pip python3-venv


cp ../settings.ini.example /etc/pigateman.ini
cp pigateman.service /etc/systemd/system/pigateman.service
touch /var/log/pigateman-door.log
touch /var/log/pigateman.log
cp pigateman_nginx.conf /etc/nginx/sites-enabled/pigateman.conf
# need to handle letsencrypt stuff here!


mkdir -p /opt/pigateman
cp -r ../* /opt/pigateman
cd /opt/pigateman

virtualenv -p python3 venv
pip install -r requirements.txt
systemctl daemon-reload
systemctl enable pigateman
echo "You need to configure /etc/pigateman.ini before running systemctl start pigateman"

