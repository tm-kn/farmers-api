import os

from .base import *

DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
