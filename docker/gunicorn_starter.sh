#!/bin/sh
gunicorn "flask_op.flask_op:create_app('/app/docker/config.py')" -b 0.0.0.0:8000 --certfile keys/local.crt --keyfile keys/local.key