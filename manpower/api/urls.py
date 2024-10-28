from rest_framework import routers
from django.urls import path

from .views import ManpowerViewSet, UpdateManpowerStatus, ManpowerStatistics

router = routers.SimpleRouter()
router.register(r'', ManpowerViewSet, basename='manpower')

urlpatterns = [
    path('<uuid:pk>/update-status/', UpdateManpowerStatus.as_view(), name='update_manpower_status'),
    path('statistics/', ManpowerStatistics.as_view(), name='manpower_statistics'),
] + router.urls
