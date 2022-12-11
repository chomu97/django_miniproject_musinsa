#!/bin/bash

echo "===== django start ========"

# python django_start.py

nohup python manage.py runserver 0.0.0.0:9000 &

echo "====== shell end ===="