#!/bin/bash
echo "==== find process ===="
ps -ef | grep runserver

echo "==== kill process ===="
pkill -f runserver

echo "=== after kill process ==="
ps -ef | grep runserver