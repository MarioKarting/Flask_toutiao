#! /bin/bash
source ~/.bashrc
export PYTHONPATH=/root/config:$PYTHONPATH
export FLASK_ENV=production
export TOUTIAO_WEB_SETTINGS=/root/config/web_deploy.py
export TOUTIAO_CELERY_SETTINGS=celery_deploy.CeleryConfig
cd /root/toutiao-backend/
workon toutiao
exec gunicorn -b 0.0.0.0:8000 --access-logfile /root/logs/access_app.log --error-logfile /root/logs/error_app.log toutiao.main:app