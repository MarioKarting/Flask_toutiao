from celery import Celery
from settings.default import CeleryConfig

app = Celery('toutiao')
app.config_from_object(CeleryConfig)
app.config_from_envvar('TOUTIAO_CELERY_SETTINGS', silent=True)

app.autodiscover_tasks(['celery_tasks.sms'])


