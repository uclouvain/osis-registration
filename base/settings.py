"""
Django settings for osis_registration project.
"""

import os

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# MOCK LDAP SERVICE CALLS
MOCK_LDAP_CALLS = os.environ.get('MOCK_LDAP_CALLS', 'True').lower() == 'true'

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split()

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'LOCAL')

APPLICATION_TOKEN = os.environ.get('APPLICATION_TOKEN', '')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'ckeditor',
    'statici18n',
    'rest_framework',
    'base',
    'captcha',
    'bootstrap3',
    'rest_framework.authtoken'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'base.middleware.auto_detect_lang.AutoDetectLanguage',
]

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'base/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'base.views.common.common_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'base.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("DATABASE_NAME", 'osis_registration_local'),
        'USER': os.environ.get("POSTGRES_USER", 'osis'),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD", 'osis'),
        'HOST': os.environ.get("POSTGRES_HOST", '127.0.0.1'),
        'PORT': os.environ.get("POSTGRES_PORT", '5432'),
        'ATOMIC_REQUESTS':  os.environ.get('DATABASE_ATOMIC_REQUEST', 'True').lower() == 'true'
    },
}


# Password validation

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


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


STATICFILES_DIRS = (os.path.join(BASE_DIR, 'base/static'),)
STATICI18N_ROOT = os.path.join(BASE_DIR, os.environ.get('STATICI18N', 'base/static'))

LDAP_ACCOUNT_CREATION_URL = os.environ.get('LDAP_ACCOUNT_CREATION_URL', '')
LDAP_ACCOUNT_DELETION_URL = os.environ.get('LDAP_ACCOUNT_DELETION_URL', '')
LDAP_ACCOUNT_MODIFICATION_URL = os.environ.get('LDAP_ACCOUNT_MODIFICATION_URL', '')
LDAP_ACCOUNT_DESCRIBE_EMAIL_URL = os.environ.get('LDAP_ACCOUNT_DESCRIBE_EMAIL_URL', '')
LDAP_ACCOUNT_IS_SWITCHED_EMAIL_URL = os.environ.get('LDAP_ACCOUNT_IS_SWITCHED_EMAIL_URL', '')
LDAP_ACCOUNT_VALIDITY_DAYS = os.environ.get('LDAP_ACCOUNT_VALIDITY_DAYS', 120)

PASSWORD_CHECK_URL = os.environ.get('PASSWORD_CHECK_URL', '')

OSIS_PORTAL_URL = os.environ.get('OSIS_PORTAL_URL', '')
ADMISSION_LOGIN_URL = os.environ.get('ADMISSION_LOGIN_URL', '')
LOST_PASSWORD_URL = os.environ.get('LOST_PASSWORD_URL', '')
LOST_PASSWORD_LDAP_URL = os.environ.get('LOST_PASSWORD_LDAP_URL', '')

DATA_PROTECTION_POLICY_URL = os.environ.get('DATA_PROTECTION_POLICY_URL', '')

DEFAULT_LOGGER = os.environ.get('DEFAULT_LOGGER', 'default')

CAPTCHA_FONT_SIZE = 50
CAPTCHA_IMAGE_SIZE = (300, 80)
CAPTCHA_LENGTH = 6
CAPTCHA_FOREGROUND_COLOR = '#163c69'

CAPTCHA_FLITE_PATH = '/usr/bin/espeak'
CAPTCHA_SOX_PATH = '/usr/bin/sox'

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
# If you want to change the default settings,
# you have to redefine the LANGUAGE_CODE and LANGUAGES vars in environment settings (ex: dev.py)
LANGUAGES = [
    ('fr-be', _('French')),
    ('en', _('English')),
]
LANGUAGE_CODE_FR = 'fr-be'
LANGUAGE_CODE_EN = 'en'

LANGUAGE_CODE = 'fr-be'

LANGUAGE_COOKIE_NAME = "language"

TIME_ZONE = os.environ.get('TIME_ZONE', 'Europe/Brussels')

USE_I18N = os.environ.get('USE_I18N', 'True').lower() == 'true'
USE_L10N = os.environ.get('USE_L10N', 'True').lower() == 'true'
USE_TZ = os.environ.get('USE_TZ', 'False').lower() == 'true'

SEND_MAIL_LOGGER = os.environ.get('SEND_MAIL_LOGGER', 'send_mail')

# Email Settings
# By default Email are saved in the folder defined by EMAIL_FILE_PATH
# If you want ti use the smtp backend,
# you have to define EMAIL_BACKEND, EMAIL_HOST and EMAIL_PORT in your .env if the default values doesn't match.
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'osis@localhost.be')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', DEFAULT_FROM_EMAIL)
LOGO_EMAIL_SIGNATURE_URL = os.environ.get('LOGO_EMAIL_SIGNATURE_URL', '')
EMAIL_PRODUCTION_SENDING = os.environ.get('EMAIL_PRODUCTION_SENDING', 'False').lower() == 'true'
COMMON_EMAIL_RECEIVER = os.environ.get('COMMON_EMAIL_RECEIVER', 'osis@localhost.org')
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.filebased.EmailBackend')
EMAIL_FILE_PATH = os.environ.get('EMAIL_FILE_PATH', os.path.join(BASE_DIR, "messaging/sent_mails"))
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 25))
SEND_BROKEN_LINK_EMAILS = os.environ.get('SEND_BROKEN_LINK_EMAILS', 'True').lower() == 'true'
MAIL_SENDER_CLASSES = os.environ.get(
    'MAIL_SENDER_CLASSES',
    'base.messaging.mail_sender_classes.MessageHistorySender'
).split()

LOGO_OSIS_URL = os.environ.get('LOGO_OSIS_URL', '')

APPLICATION_URL = os.environ.get('APPLICATION_URL', '')

# set token validity to 24 hours
PASSWORD_RESET_TIMEOUT = 86400

REQUESTS_RATE_LIMIT = os.environ.get('REQUESTS_RATE_LIMIT', '10/h')
RESET_SEND_MAIL_RATE_LIMIT = os.environ.get('RESET_SEND_MAIL_RATE_LIMIT', '1/10s')

REJECTED_EMAIL_DOMAINS = os.environ.get('REJECTED_EMAIL_DOMAINS', "uclouvain.be").split()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'default': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'event': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

REGISTRATION_CALENDAR_URL_FR = os.environ.get('REGISTRATION_CALENDAR_URL_FR', '')
REGISTRATION_CALENDAR_URL_EN = os.environ.get('REGISTRATION_CALENDAR_URL_EN', '')

STUDY_PROGRAMME_URL_FR = os.environ.get('STUDY_PROGRAMME_URL_FR', '')
STUDY_PROGRAMME_URL_EN = os.environ.get('STUDY_PROGRAMME_URL_EN', '')

PROGRAMME_REQUIREMENTS_URL_FR = os.environ.get('PROGRAMME_REQUIREMENTS_URL_FR', '')
PROGRAMME_REQUIREMENTS_URL_EN = os.environ.get('PROGRAMME_REQUIREMENTS_URL_EN', '')

FAQ_URL_FR = os.environ.get('FAQ_URL_FR', '')
FAQ_URL_EN = os.environ.get('FAQ_URL_EN', '')

CONTACT_URL_FR = os.environ.get('CONTACT_URL_FR', '')
CONTACT_URL_EN = os.environ.get('CONTACT_URL_EN', '')

TUITION_FEES_URL_FR = os.environ.get('TUITION_FEES_URL_FR', '')
TUITION_FEES_URL_EN = os.environ.get('TUITION_FEES_URL_EN', '')

PASSERELLES_URL_FR = os.environ.get('PASSERELLES_URL_FR', '')
PASSERELLES_URL_EN = os.environ.get('PASSERELLES_URL_EN', '')

FUNDING_ELIGIBILITY_URL_FR = os.environ.get('FUNDING_ELIGIBILITY_URL_FR', '')
FUNDING_ELIGIBILITY_URL_EN = os.environ.get('FUNDING_ELIGIBILITY_URL_EN', '')

ACCOMMODATIONS_URL_FR = os.environ.get('ACCOMMODATIONS_URL_FR', '')
ACCOMMODATIONS_URL_EN = os.environ.get('ACCOMMODATIONS_URL_EN', '')

PREPARING_ARRIVAL_URL_FR = os.environ.get('PREPARING_ARRIVAL_URL_FR', '')
PREPARING_ARRIVAL_URL_EN = os.environ.get('PREPARING_ARRIVAL_URL_EN', '')

ASSIMILATION_URL_FR = os.environ.get('ASSIMILATION_URL_FR', '')
ASSIMILATION_URL_EN = os.environ.get('ASSIMILATION_URL_EN', '')
