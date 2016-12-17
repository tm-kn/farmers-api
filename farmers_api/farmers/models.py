from django.db import models
from django.utils.translation import ugettext_lazy as _


class Farmer(models.Model):
    first_name = models.CharField(_('first name'), max_length=50)
    surname = models.CharField(_('surname'), max_length=50)
    town = models.CharField(_('town'), max_length=50)

    class Meta:
        verbose_name = _('farmer')
        verbose_name_plural = _('farmers')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.surname)

    def get_short_name(self):
        return '%s. %s' % (self.first_name[:1], self_surname)
