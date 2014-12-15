# coding:utf-8
# Django 1.6 settings for operation project.
import os
from django.utils.translation import ugettext_lazy as _

LOG_ROOT = '/tmp'
DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_OPERATION = 'operation'
FILE_CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.dirname(FILE_CURRENT_PATH)
root_index = FILE_CURRENT_PATH.find(BASE_OPERATION)
SITE_ROOT = FILE_CURRENT_PATH[:root_index + len(BASE_OPERATION) + 1]

SECRET_KEY = 'elgw@*53y*q&0i&g_$5c1-lj$ks-h2a9lhve@(9l4#qerz@049'
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = (
    'operation.core.customs',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cadmin',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'


# Database
MONGODB_CONF = 'mongodb://10.6.7.200:27017'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'public',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
    }
}


# Language
LANGUAGE_CODE = 'zh-cn'
LANGUAGES = (
    ('zh-cn', u'简体中文'),
    ('en', 'English'),
)
# date and datetime field formats
TIME_ZONE = 'Asia/Shanghai'
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (
    '%s/%s' % (PROJECT_ROOT, '/locale'),
    '%s/%s' % (SITE_ROOT, '/core/locale')
)

# Static
STATIC_URL = '/static/'
MEDIA_ROOT = '/var/app/data'
MEDIA_URL = 'http://localhost/'
STATIC_ROOT = '/var/app/enabled/seabedop-webfront/static'
#STATICFILES_DIRS = (,)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

# Grappelli
GRAPPELLI_AUTOCOMPLETE_LIMIT = 50
GRAPPELLI_ADMIN_TITLE = "Public Service"
GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'


# Logger
LOG_FILE = os.path.join(LOG_ROOT, 'info.log')
LOG_ERR_FILE = os.path.join(LOG_ROOT, 'error.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'detail': {
            'format':
            '%(levelname)s %(asctime)s %(name)s [%(module)s.%(funcName)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'formatter': 'detail',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOG_FILE,
        },
        'err_file': {
            'level': 'ERROR',
            'formatter': 'detail',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOG_ERR_FILE,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'err_file', ]
            if DEBUG else ['file', 'err_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'operation': {
            'handlers': ['console', 'file', 'err_file', ]
            if DEBUG else ['file', 'err_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'core': {
            'handlers': ['console', 'file', 'err_file', ]
            if DEBUG else ['file', 'err_file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}


APP_MENU_LIST = {
    'cadmin': {
        'title': 'abc',
        'models': {'cadmin.models.PushMessage': {'title': 'push message', 'order': 2}},
        'order': 1,
    },
    'auth': {
        'title': 'Auth',
        'models': {
            'django.contrib.auth.models.Group': {'title': 'Group', 'order': 1},
            'django.contrib.auth.models.User': {'title': 'User', 'order': 2},
            'django.contrib.admin.models.LogEntry': {'title': _('Admin Log'), 'order': 3},
        },
        'order': 2,
    }
}
