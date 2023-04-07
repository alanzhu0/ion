#!/bin/sh
cp -u config/docker/secret.py intranet/settings

echo "Performing pre-startup tasks..."
python3 -u config/docker/entrypoint.py &  # For initial setup
sass --watch intranet/static/css:intranet/collected_static/css &  # Automatically compile modified scss files

python3 manage.py runserver 0.0.0.0:8080
