#!/usr/bin/env bash

uv run manage.py collectstatic --noinput
uv run manage.py migrate --noinput
uv run -m gunicorn --bind 0.0.0.0:8004 --workers 3 brdtheo.wsgi:application