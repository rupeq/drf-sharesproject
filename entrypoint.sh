#!/bin/bash

python3 manage.py migrate --noinput
python3 manage.py runserver 0.0.0.0:8000
python3 manage.py initadmin
