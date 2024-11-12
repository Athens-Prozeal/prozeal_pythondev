from django.urls import path
from rest_framework import routers

from .views import GeneralPtwViewSet, VerifyGeneralPtw, ClientApproveGeneralPtw, ClientRejectGeneralPtw, ClosureRequestGeneralPtw, CloseGeneralPtw

router = routers.SimpleRouter()

router.register('general', GeneralPtwViewSet, basename='general-ptw')

urlpatterns = [
    path('general/<uuid:pk>/verify/', VerifyGeneralPtw.as_view(), name='verify-general-ptw'),
    path('general/<uuid:pk>/client-approve/', ClientApproveGeneralPtw.as_view(), name='client-approve-general-ptw'),
    path('general/<uuid:pk>/client-reject/', ClientRejectGeneralPtw.as_view(), name='client-reject-general-ptw'),
    path('general/<uuid:pk>/closure-request/', ClosureRequestGeneralPtw.as_view(), name='closure-request-general-ptw'),
    path('general/<uuid:pk>/close/', CloseGeneralPtw.as_view(), name='close-general-ptw'),

] + router.urls
