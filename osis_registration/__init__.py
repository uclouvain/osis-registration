from .celery import app as celery_app

# Do not remove because signal will not be registered
default_app_config = 'osis_registration.apps.OsisRegistrationConfig'
