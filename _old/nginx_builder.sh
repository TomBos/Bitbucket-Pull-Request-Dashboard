#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
NGINX_CONF="deploy/bitbucket-pull-request-dashboard.conf"

cp "$SCRIPT_DIR/deploy/template.conf" "$SCRIPT_DIR/$NGINX_CONF"
sed -i "s|_ROOT_PATH_|$(realpath public/)|g" "$SCRIPT_DIR/$NGINX_CONF"

if [[ ! -d "/etc/nginx/conf.d/" ]];then
	sudo mkdir -p "/etc/nginx/conf.d/"
fi

sudo ln -sf "$SCRIPT_DIR/$NGINX_CONF" "/etc/nginx/conf.d/" 
sudo systemctl reload nginx

