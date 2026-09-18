from django.contrib import admin
from django.urls import path,include

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        "status": "ok",
        "message": "ResultPortal API",
        "docs": "/swagger/"
    })

urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/', include('academics.urls')),
    path('api/', include('account.urls')),
    path('api/', include('results.urls')),
    path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]