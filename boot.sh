#! /bin/bash
flask db upgrade

gunicorn --bind 0.0.0.0:5000 --timeout 200 --workers=2 run:app