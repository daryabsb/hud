from src.settings.components.env import config


REDIS_HOST = config('REDIS_HOST', default='127.0.0.1')
REDIS_PORT = config("REDIS_PORT", default=6378)

REDIS_URL = f'redis://{REDIS_HOST}:{str(REDIS_PORT)}'