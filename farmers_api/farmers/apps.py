from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FarmersConfig(AppConfig):
    name = 'farmers'
    verbose_name = _('Farmers')
