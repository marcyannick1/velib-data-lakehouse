#!/bin/bash

set -e

export PGPASSWORD=velib_password

echo "Creating tables..."

psql \
-h postgres \
-U velib_user \
-d velib \
-f /opt/project/postgres/init.sql

echo "Creating views..."

psql \
-h postgres \
-U velib_user \
-d velib \
-f /opt/project/analytics/analytics.sql

echo "Database initialized"