#!/bin/bash

set -eu

echo "==> Executing database migrations"
/app/code/env/bin/python /app/code/baserow/backend/src/baserow/manage.py migrate --settings=cloudron.settings

chown -R cloudron:cloudron /app/data

echo "==> Starting"
exec /usr/bin/supervisord --configuration /etc/supervisor/conf.d/supervisor.conf
