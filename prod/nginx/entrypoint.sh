#!/bin/sh

envsubst '${NGINX_API_PROXY} ${NGINX_API_HOST}' < /nginx.conf.template > /etc/nginx/conf.d/app.conf

exec "$@"
