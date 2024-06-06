@echo off
python manage.py makemigrations user
python manage.py makemigrations equipment
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
python manage.py initadmin
python manage.py loaddata fixtures/gods.json
