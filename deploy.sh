#!/bin/bash


sudo apt install letsencrypt
sudo certbot certonly --standalone -d ncov.1337.rip --agree-tos
sudo chown -R $SUDO_USER:$SUDO_USER /etc/letsencrypt
docker-compose up