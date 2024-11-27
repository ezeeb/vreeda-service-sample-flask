#!/usr/bin/env bash

docker compose up -d

. .venv/bin/activate

pip install -r requirements.txt

flask run --debug
