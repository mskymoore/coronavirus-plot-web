#!/bin/bash

sudo su
apt install letsencrypt
sudo certbot certonly --standalone -d ncov.1337.rip
chown -R admin:admin /etc/letsencrypt
docker-compose up