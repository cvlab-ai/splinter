#!/bin/bash

mkdir -p /etc/apache2/
htpasswd -b -c /etc/apache2/.htpasswd_splinter ${EX_STORE_SPLINTER_USER} ${EX_STORE_SPLINTER_PASS}
htpasswd -b -c /etc/apache2/.htpasswd_webdav ${EX_STORE_WEBDAV_USER} ${EX_STORE_WEBDAV_PASS}
