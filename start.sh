#!/usr/bin/env sh

gunicorn vision:app --bind=0.0.0.0:8000
