#!/bin/bash
set -e

DOMAIN=${1:?"Укажите домен: sudo bash deploy.sh example.com"}
REPO=https://github.com/kuzoVS/TaskReload.git
APP=/opt/notes

apt-get update
apt-get install -y python3 python3-pip git nginx certbot python3-certbot-nginx

if [ -d "$APP/.git" ]; then
    git -C "$APP" pull
else
    git clone -b python "$REPO" "$APP"
fi
cd "$APP/notes_site"

pip3 install --break-system-packages -r requirements.txt

if [ ! -f /etc/notes.env ]; then
    echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" > /etc/notes.env
fi
grep -q '^ALLOWED_HOSTS=' /etc/notes.env || echo "ALLOWED_HOSTS=$DOMAIN" >> /etc/notes.env
chmod 600 /etc/notes.env

chown -R www-data:www-data "$APP/notes_site"
sudo -u www-data bash -c "set -a; . /etc/notes.env; python3 manage.py migrate --noinput; python3 manage.py collectstatic --noinput"

cp deploy/notes.service /etc/systemd/system/notes.service
systemctl daemon-reload
systemctl enable notes
systemctl restart notes

sed "s/DOMAIN/$DOMAIN/" deploy/nginx.conf > /etc/nginx/sites-available/notes
ln -sf /etc/nginx/sites-available/notes /etc/nginx/sites-enabled/notes
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --register-unsafely-without-email --redirect
grep -q '^HTTPS=1' /etc/notes.env || echo "HTTPS=1" >> /etc/notes.env
systemctl restart notes

echo "Готово: https://$DOMAIN"
