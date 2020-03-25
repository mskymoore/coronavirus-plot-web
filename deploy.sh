#!/bin/bash

sudo apt install letsencrypt
certbot certonly --standalone -d ncov.1337.rip
docker-compose up