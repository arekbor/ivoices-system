#!/bin/bash

if [ -z "$1" ]
then
    echo "You must pass migration name"
    exit 1
fi

alembic revision -m "$1"
exit 0