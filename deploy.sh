#!/bin/bash

sudo su
apt install letsencrypt
certbot certonly --standalone -d ncov.1337.rip
chown -R admin:admin /etc/letsencrypt
exit
docker-compose up