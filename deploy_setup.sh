#!/bin/bash

# This script is meant to automate setup work before deploying to production
# environment. The script will:
# * generate random passwords for docker services & replace them in .env file
# * generate docker-compose file compatible with docker swarm e.g include
#   content of .env file to each service depending on it


bold=$(tput bold)
normal=$(tput sgr0)

gen_password() {
    cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1
}

SWARM_COMPOSE_FILE="docker-compose-swarm.yml"

echo "Preparing project for deploying on docker swarm..."

echo "Generating random passwords..."
EX_STORE_SPLINTER_PASS="$(gen_password)"
EX_STORE_WEBDAV_PASS="$(gen_password)"
POSTGRES_PASSWORD="$(gen_password)"
sed -i -r "s/^(EX_STORE_SPLINTER_PASS=).*/\1\"${EX_STORE_SPLINTER_PASS}\"/" .env
sed -i -r "s/^(EX_STORE_WEBDAV_PASS=).*/\1\"${EX_STORE_WEBDAV_PASS}\"/" .env
sed -i -r "s/^(POSTGRES_PASSWORD=).*/\1\"${POSTGRES_PASSWORD}\"/" .env

echo 
echo "###############################################################################"
echo "#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!SAVE THIS INFO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#"
echo "#                                                                             #"
echo "# Passwords generated for services:                                           #"
echo "# EX_STORE_SPLINTER_PASS=\"${EX_STORE_SPLINTER_PASS}\"                                       #"
echo "# EX_STORE_WEBDAV_PASS=\"${EX_STORE_WEBDAV_PASS}\"                                         #"
echo "# POSTGRES_PASSWORD=\"${POSTGRES_PASSWORD}\"                                            #"
echo "#                                                                             #"
echo "###############################################################################"
echo

docker-compose config > ${SWARM_COMPOSE_FILE}
echo "Docker Compose configuration done"
echo "Please use ${bold}${SWARM_COMPOSE_FILE}${normal} to deploy the stack."
