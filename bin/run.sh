#!/bin/bash
SECRETS_FILE=/run/secrets/env-events

export $(cat $SECRETS_FILE)

if [ "$1" = "web" ]
then
    exec uwsgi --master -w main:app --http 0.0.0.0:5000 --enable-threads
elif [ "$1" = "worker" ]
then
    exec python -u worker.py
fi
