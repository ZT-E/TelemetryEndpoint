export FLASK_HOST=
export FLASK_APP=app.py
export FLASK_ENV=production
export FLASK_SECRET=
export WEBHOOK_URL=
export PUBLIC_SITE=
/usr/bin/gunicorn --bind 127.0.0.1:1919 app:app
