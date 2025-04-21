from src.settings.components.env import config


REDIS_HOST = config('REDIS_HOST', default='192.168.1.8')
REDIS_PORT = config("REDIS_PORT", default=6378)

REDIS_URL = f'redis://{REDIS_HOST}:{str(REDIS_PORT)}'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # Replace with your Memurai server's address and port
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
