from src.settings.components.redis import REDIS_HOST, REDIS_PORT
from src.settings.components.secretes import CELERY_BROKER_DB, CELERY_RESULT_DB
# from src.settings.components.common import TIME_ZONE

#: Redis redis://:password@hostname:port/db_number
BROKER_URL = 'redis://{host}:{port}/{db}'.format(
    host=REDIS_HOST, port=REDIS_PORT, db=CELERY_BROKER_DB)
# BROKER_URL = 'redis://:ZKSoft3@127.0.0.1:7396/1'
CELERY_RESULT_BACKEND = 'redis://{host}:{port}/{db}'.format(
    host=REDIS_HOST, port=REDIS_PORT, db=CELERY_RESULT_DB)
DJANGO_CELERY_BEAT_TZ_AWARE = False
# #: Only add pickle to this list if your broker is secured
# #: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'json'

# CELERY_TASK_RESULT_EXPIRES = 5 * 60
# CELERY_ENABLE_UTC = True
# CELERY_TIMEZONE = TIME_ZONE
# CELERYD_FORCE_EXECV = True
# CELERYD_CONCURRENCY = 3
# CELERYD_MAX_TASKS_PER_CHILD = 100
# CELERY_IGNORE_RESULT = True

# CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"
