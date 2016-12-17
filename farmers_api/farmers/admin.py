from django.contrib import admin

from .models import Farmer


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    pass
