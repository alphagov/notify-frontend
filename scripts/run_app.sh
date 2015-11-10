#!/bin/bash
if [ -n "$VIRTUAL_ENV" ]; then
  echo "Already in virtual environment $VIRTUAL_ENV"
else
  source ./venv/bin/activate 2>/dev/null && echo "Virtual environment activated."
fi
export NOTIFY_ADMIN_FRONTEND_COOKIE_SECRET=${NOTIFY_ADMIN_FRONTEND_COOKIE_SECRET:=secret}


python application.py runserver
