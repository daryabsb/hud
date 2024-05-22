from src.settings.components.env import config
# from src.settings.components.config_file import CONFIG_FILE

DEBUG = config('DEBUG', default=1)
SECRET_KEY = config("DJANGO_SECRET_KEY", default=None)
# PIN_WIDTH = CONFIG_FILE.getint('SYS', 'PIN_WIDTH', fallback=0)
# ID_FOR_PIN = CONFIG_FILE.getint('SYS', 'ID_FOR_PIN', fallback=0)
# IMPORT_TRANS = CONFIG_FILE.getint('SYS', 'IMPORT_TRANS', fallback=0)

# ATT_WITHOUT_SECOND = CONFIG_FILE.getint('SYS', 'ATT_WITHOUT_SECOND', fallback=1)

# SERVER_TYPE = CONFIG_FILE.get('Options', 'Type', fallback='WSGI')
# SERVER_PORT = CONFIG_FILE.get('Options', 'Port', fallback='80')

# VM_DETECT = CONFIG_FILE.getint('SYS', 'VM_DETECT', fallback=0)

# because 'get_from_env_or_file' function return always string type
# first try convert str type to int type to compatible enterprise edition
try:
    DEBUG = int(DEBUG)
except ValueError:
    if DEBUG == 'true':
        DEBUG = 1
    else:
        DEBUG = 0

CELERY_BROKER_DB = config('CELERY_BROKER_DB', default=1)
CELERY_RESULT_DB = config('CELERY_RESULT_DB', default=2)


ALLOWED_HOSTS = ['172.16.10.49']
ALLOWED_HOST = config("ALLOWED_HOST", cast=str, default="")
if ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(ALLOWED_HOST.strip())

# if environ.get('SECRET_KEY') is None:
#     SECRET_KEY_SUFFIX = config('SECRET_KEY', default=str(uuid.getnode()))
#     if not SECRET_KEY_SUFFIX:
#         SECRET_KEY_SUFFIX = str(uuid.getnode())

#     BASE_SECRETE = '=Q6(Zc:7ad>}s6ZF?B7;dTCgHf\#^G*}(ey:Wc7J6fG@:9YU&D'
#     SECRET_KEY = BASE_SECRETE[:35] + SECRET_KEY_SUFFIX[:15]
# else:
#     SECRET_KEY = environ.get('SECRET_KEY')

# RESTARTAPACHE = CONFIG_FILE.get('SYS', 'RESTARTAPACHE', fallback=0)
# WRITE_LOG = CONFIG_FILE.getint('SYS', 'WRITE_LOG', fallback=1)
# NOEXPORT = CONFIG_FILE.getint('SYS', 'NOEXPORT', fallback=0)
# SHOWEMPPHOTO = CONFIG_FILE.getint('SYS', 'SHOW_PHOTO', fallback=1)
# DEMO = CONFIG_FILE.getint('SYS', 'DEMO', fallback=0)
# LICENSEURL = CONFIG_FILE.get('SYS', 'LICENSE_URL', fallback='')
# WHATSAPP_API_URL = CONFIG_FILE.get('SYS', 'WHATSAPP_API_URL', fallback='')
# MD5FILES = CONFIG_FILE.get('SYS', 'MD5', fallback='')
# IP_BY_DEVICE = CONFIG_FILE.getint('SYS', 'IPAddressByDevice', fallback=1)
# DOUBLE_WALLET = CONFIG_FILE.getint('SYS', 'DOUBLE_WALLET', fallback=0)
# REMOTE_UPGRADE = CONFIG_FILE.getint('SYS', 'REMOTE_UPGRADE', fallback=0)
# UPGRADE_PASSWORD = CONFIG_FILE.get('SYS', 'UPGRADE_PASSWORD', fallback='')
# FILTER_BY_HIRE_DAY = CONFIG_FILE.getint('SYS', 'FILTER_BY_HIRE_DAY', fallback=0)
# PRODUCT_CODE = CONFIG_FILE.getint('SYS', 'PRODUCT_CODE', fallback=15)  # 8=wdms  9=biotime
# TRANSLATE_OPTION_STATUS = CONFIG_FILE.getint('SYS', 'TRANSLATE_OPTION_STATUS', fallback=0)

# ACTIVE_CELERY = CONFIG_FILE.getint('CELERY', 'ACTIVE_CELERY', fallback=0)

# LANGUAGE_CODE = config('SYS', 'LANGUAGE_CODE', default='en')

# STD_DATETIME_FORMAT = config('SYS', 'STD_DATETIME_FORMAT', default='%Y-%m-%d %H:%M:%S')
# STD_DATE_FORMAT = config('SYS', 'STD_DATE_FORMAT', default='%m/%d/%Y')
# STD_TIME_FORMAT = config('SYS', 'STD_TIME_FORMAT', default='%H:%M:%S')

# DEVICE_TIME_ZONE = config('DEVICE', 'TIMEZONE', default=330)
# THAILAND = config('SYS', 'THAILAND', default=0)

# HOST = config('Options', 'HOST', default='127.0.0.1')
# PORT = config('Options', 'Port', default=80)
# PORT0 = config('Options', 'Port0', default=20001)
# TYPE = config('Options', 'Type', default='WSGI').lower()
# SERVICES = config('Options', 'Services', default=0)
# OEM_CODE = config('Options', 'OEM', default='')
