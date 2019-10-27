# PiGateMan Home Automation

This project is intended to be a home automation solution. Conceived from wanting an automated way to open an electronically controlled gate with a rasberry pi and gpio.

Currently it only supports triggering relays via API transaction.

# Deployment
Deployment is on rasbian, the debian variant for rasberry pis.
Included is the systemd unit file to run gunicorn as a service. The service is configured to startup with the OS at boot time
`/etc/systemd/system/pigateman.service`
To reconfigure this you can run.
`systemctl enable pigateman` or `systemctl disable pigateman`

The application code is deployed in /opt/pigateman.

The gunicorn processes sit behind a nginx reverse proxy which point to the gunicorn process at 127.0.0.1:8000.
The nginx reverse proxy is setup to listen for SSL connections on port 443, and use a SSL certificate from let's encrypt for the applicable domain.
The nginx conf file is included in the deployment directory of this repo( deployed to /etc/nginx/sites-enabled/pigateman )


# SSL certificate renewal. 
There is a cronjob configured to renew let's encrypt certificates using certbot.
`0 0 05 10,26 * ? systemctl stop nginx; certbot certonly --standalone -d entry.luac.es; systemctl start nginx;`

# Updating
- Copy repo contents to /opt/pigateman
- Update /etc/nginx/sites-enabled/pigateman if applicable.
- Update /etc/systemd/system/pigateman.service if applicable.
- Run `systemctl daemon-reload` if the service unit file above was updated.
- Run systemctl restart pigateman to restart the service post update.


# Relevant Documentation
- https://certbot.eff.org/
- https://www.raspberrypi.org/documentation/usage/gpio/