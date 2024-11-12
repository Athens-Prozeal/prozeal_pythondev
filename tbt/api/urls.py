from rest_framework import routers

from .views import TbtViewSet

router = routers.SimpleRouter()
router.register(r'', TbtViewSet, basename='tbt')

urlpatterns = router.urls
