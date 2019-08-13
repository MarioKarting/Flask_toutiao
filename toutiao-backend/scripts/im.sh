#! /bin/bash
source ~/.bashrc
export PYTHONPATH=/root/config:$PYTHONPATH
export FLASK_ENV=production
export TOUTIAO_WEB_SETTINGS=/root/config/web_deploy.py
export TOUTIAO_CELERY_SETTINGS=celery_deploy.CeleryConfig
cd /root/toutiao-backend/im/
workon toutiao
exec python main.py 8001