#!/usr/bin/env bash


npm i
npm run build


python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

sudo apt install gunicorn

gunicorn --workers 4 --bind 0.0.0.0:8100 'main:app'
