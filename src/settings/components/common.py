from src.settings.components.env import config
from tzlocal import get_localzone
from src.settings.components import PROJECT_PATH

from src.settings.components.redis import REDIS_HOST, REDIS_PORT

BASE_ENDPOINT = config('BASE_ENDPOINT', default='http://127.0.0.1:8000')
WS_ENDPOINT = config('WS_ENDPOINT', default='ws://127.0.0.1:8000')

# Application definition
SITE_ID = 1

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'allauth',
    'allauth.account',
    "django_extensions",
    "django_htmx",
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'after_response',
    'rest_framework',

]

THIRD_PARTY_APPS = [
    'src._utils',
    'widget_tweaks',
    'mptt',
    'fontawesome_5',
    'colorfield',
    'django_filters',
    'rest_framework_datatables',
    # 'table',
    "django_tables2",
    'datatableview',
    'src.games',
]

LOCAL_APPS = [
    'src.accounts',
    'src.core',
    'src.configurations',
    'src.documents',
    'src.finances',
    'src.pos',
    'src.management',
    'src.products',
    'src.orders',
    'src.printers',
    'src.tax',
    'src.stock',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # or 'mandatory'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_PATH + "\\templates",
            PROJECT_PATH + "\\accounts\\templates",
            PROJECT_PATH + "\\pos\\templates",
            PROJECT_PATH + "\\management\\templates",
            PROJECT_PATH + "\\configurations\\templates",
            PROJECT_PATH + "\\finances\\templates",
            PROJECT_PATH + "\\documents\\templates",
            PROJECT_PATH + "\\orders\\templates",
            PROJECT_PATH + "\\games\\templates",

        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'custom_context_processor.dz_static',
                'custom_context_processor.props',
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'
ASGI_APPLICATION = 'src.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = str(get_localzone())

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
