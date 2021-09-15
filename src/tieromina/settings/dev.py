from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^mm-24*i-6iecm7c@z9l+7%^ns^4g^z!8=dgffg4ulggr-4=1%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEV_VERSION = True

ALLOWED_HOSTS = [
    '.tieromina.acdh-dev.oeaw.ac.at', '.tieromina.hephaistos.arz.oeaw.ac.at',
    '127.0.0.1'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'tieromina',
        'USER': 'tieromina',
        'PASSWORD': 'WwxPNtMh5SjS',
        'HOST': 'helios.arz.oeaw.ac.at',
        'PORT': '5432',
    }
}

Z_ID = "1****5"
Z_ID_TYPE = 'groups'  # or 'user'
Z_COLLECTION = "*****Z"
Z_API_KEY = "T******************A"
Z_COLLECTION_URL = "https://www.zotero.org/{}/{}/peter_handke_stage_texts".format(
    Z_ID, Z_COLLECTION)
Z_TITLE = "Some Titel of the Zotero Library"
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(name)-15s %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
# LOGGING = {
#     'version': 1,
#     'formatters': {
#         'simple': {
#             'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
#             'style': '{'
#         }
#     },
#     'filters': [],
#     'handlers': [],
#     'datefmt': '%Y-%m-%d %H:%M:%S'
# }
