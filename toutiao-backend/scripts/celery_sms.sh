#! /bin/bash
source ~/.bashrc
export PYTHONPATH=/root/config:$PYTHONPATH
export FLASK_ENV=production
export TOUTIAO_WEB_SETTINGS=/root/config/web_deploy.py
export TOUTIAO_CELERY_SETTINGS=celery_deploy.CeleryConfig
cd /root/toutiao-backend/common
workon toutiao
exec celery -A celery_tasks.main worker -l info -Q sms