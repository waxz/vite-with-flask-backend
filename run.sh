#!/usr/bin/env bash

HASH() {
     openssl dgst -sha256 |
      LC_ALL=C sed '
        /SHA2-256(stdin)= /s/SHA2-256(stdin)=//
        s/\s//g
        '
} 


# npm
sudo npm i npm@11.2.0 -g

# nginx
sudo apt update
sudo apt install -y nginx apache2-utils

if [[ -f /etc/nginx/sites-enabled/default ]] ; then sudo unlink /etc/nginx/sites-enabled/default ;fi
sudo mkdir -p /etc/nginx/locations


# https://stackoverflow.com/questions/59895/how-do-i-get-the-directory-where-a-bash-script-is-located-from-within-the-script
SOURCE=${BASH_SOURCE[0]}
while [ -L "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
  SOURCE=$(readlink "$SOURCE")
  [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )

# env
PROJECT=vite

PORT=8000
CONTENT=$DIR/content

NGINX_DOMAIN=$PROJECT
NGINX_USER=$PROJECT
NGINX_PSW=$PROJECT


if [[ ! -z "$VITE_PORT" ]]; then PORT=$VITE_PORT;fi
if [[ ! -z "$VITE_CONTENT" ]]; then CONTENT=$VITE_CONTENT;fi
if [[ ! -z "$VITE_DOMAIN" ]]; then NGINX_DOMAIN=$VITE_DOMAIN ;fi

if [[ ! -z "$VITE_USER" ]]; then NGINX_USER=$VITE_USER; fi
if [[ ! -z "$VITE_PSW" ]]; then NGINX_PSW=$VITE_PSW;fi



CONATINER_NAME=$PROJECT-$NGINX_DOMAIN

echo PORT $PORT
echo CONTENT $CONTENT
echo NGINX_DOMAIN $NGINX_DOMAIN

echo NGINX_USER $NGINX_USER
echo NGINX_PSW $NGINX_PSW
echo CONATINER_NAME $CONATINER_NAME
if [ ! -f /etc/nginx/.htpasswd ]; then sudo htpasswd -bcB -C 10 /etc/nginx/.htpasswd $NGINX_USER $NGINX_PSW ; else sudo htpasswd -bB -C 10 /etc/nginx/.htpasswd $NGINX_USER $NGINX_PSW ;fi



# https://www.cyberciti.biz/faq/linux-md5-hash-string-based-on-any-input-string/

# password


PSW_FILE=psw.d
USER_PSW=$NGINX_USER:$NGINX_PSW
USER_PSW_SUM=$(printf "%s"  $USER_PSW | HASH)
echo $USER_PSW_SUM
if [[ -f $PSW_FILE && ! -z $(grep "$USER_PSW_SUM" "$PSW_FILE") ]]; then echo "FOUND"; else printf "%s" $USER_PSW_SUM | tee -a $PSW_FILE; fi
if [[ -f $PSW_FILE && ! -z $(grep "$USER_PSW_SUM" "$PSW_FILE") ]]; then echo "FOUND"; else printf "%s" $USER_PSW_SUM | tee -a $PSW_FILE; fi

# npm

npm i
npm run build


python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

sudo apt install gunicorn


gunicorn --workers 4 --bind 0.0.0.0:8100 'main:app'
