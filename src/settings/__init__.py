from split_settings.tools import include
from os import environ

ENV = environ.get('DJANGO_ENV') or 'local'

base_settings = [
    'components/paths.py',
    # 'components/storages/conf.py',
    'components/db.py',
    'components/cache.py',
    'components/celery.py',
    'components/common.py',
    # 'components/cors.py',
    'components/redis.py',
    'components/secretes.py',
]

include(*base_settings)