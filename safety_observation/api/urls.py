from rest_framework import routers
from django.urls import path

from .views import SafetyObservationViewSet, GetObservationClassification, SubmitCorrectiveAction, VerifyCorrectiveAction, RejectCorrectiveAction

router = routers.SimpleRouter()
router.register(r'', SafetyObservationViewSet, basename='safety_observation')

urlpatterns =  [
    path('classification/', GetObservationClassification.as_view(), name='get_observation_classification'),
    path('<uuid:pk>/corrective-action/', SubmitCorrectiveAction.as_view(), name='submit_corrective_action'),
    path('<uuid:pk>/verify/', VerifyCorrectiveAction.as_view(), name='verify_corrective_action'),
    path('<uuid:pk>/reject/', RejectCorrectiveAction.as_view(), name='reject_corrective_action'),
] + router.urls
