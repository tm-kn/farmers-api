from rest_framework import routers

from farmers.views import FarmerViewSet

router = routers.DefaultRouter()

router.register('farmers', FarmerViewSet)

urlpatterns = router.urls
