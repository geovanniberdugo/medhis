#!/bin/bash
source $HOME/.profile

# scp -r ../static/build ingeniarte2@50.116.33.180:~/sites/staging.medhis.net/src/static/
# scp -r ../static/build ingeniarte2@50.116.33.180:~/sites/ingeniarte.medhis.net/src/static/

workon SITE
git fetch
git reset --hard COMMIT

pip install -r requirements/production.txt
./manage.py migrate_schemas
./manage.py collectstatic --noinput

sudo supervisorctl restart SITE