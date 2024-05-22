from src.settings.components.secretes import DEBUG
from src.settings.components.common import INSTALLED_APPS, MIDDLEWARE, TEMPLATES

# The name of the GET variable that toggles the debug mode and
# prevents Django Compressor from performing the actual compression. Only useful for debugging.
# if DEBUG:
#     INSTALLED_APPS += ['debug_toolbar']
#     MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
#
#     COMPRESS_DEBUG_TOGGLE = 'verbatim'
#
#     # FOR_DEBUG_TOOLBAR
#     DEBUG_TOOLBAR_PANELS = [
#         'ddt_request_history.panels.request_history.RequestHistoryPanel',
#         'debug_toolbar.panels.versions.VersionsPanel',
#         'debug_toolbar.panels.timer.TimerPanel',
#         'debug_toolbar.panels.settings.SettingsPanel',
#         'debug_toolbar.panels.headers.HeadersPanel',
#         'debug_toolbar.panels.request.RequestPanel',
#         'debug_toolbar.panels.sql.SQLPanel',
#         'debug_toolbar.panels.templates.TemplatesPanel',
#         'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#         'debug_toolbar.panels.cache.CachePanel',
#         'debug_toolbar.panels.signals.SignalsPanel',
#         'debug_toolbar.panels.logging.LoggingPanel',
#         'debug_toolbar.panels.redirects.RedirectsPanel',
#         'debug_toolbar.panels.profiling.ProfilingPanel',
#     ]

TEMPLATES[0]['OPTIONS']['context_processors'].append(
    'middleware_template.get_main_domain_name'
)

DOMAIN_HOST = 'localhost'

SECURE_SSL_REDIRECT = False
