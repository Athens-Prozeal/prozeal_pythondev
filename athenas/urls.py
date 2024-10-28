"""
URL configuration for athenas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.api.urls')),
    # Menus
    path('api/tbt/', include('tbt.api.urls')),
    path('api/worker/', include('worker.api.urls')),
    path('api/manpower/', include('manpower.api.urls')),
    path('api/inspection/', include('inspection.api.urls')),
    path('api/safety-observation/', include('safety_observation.api.urls')),
    path('api/ptw/', include('ptw.api.urls')),

    # API Documentation
    path('openapi/', get_schema_view(
        title="Athenas API",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    
    path(
        "swagger-ui/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
]
