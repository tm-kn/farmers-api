from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'ci'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
