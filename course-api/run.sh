#!/bin/bash

exec python3 /usr/src/app/data/process.py &
exec python3 /usr/src/app/api.py