from rest_framework import routers

from .views import WorkerViewSet

router = routers.SimpleRouter()
router.register(r'', WorkerViewSet, basename='worker')

urlpatterns = router.urls
