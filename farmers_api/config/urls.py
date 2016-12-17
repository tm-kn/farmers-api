from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('config.urls_api')),
    url(r'^admin/', admin.site.urls),
]
