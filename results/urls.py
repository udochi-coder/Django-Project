from django.urls import path,include
from rest_framework.routers import DefaultRouter
from results import views


router = DefaultRouter()
router.register("result",views.ResultViewSet,"result")

urlpatterns = [
    path('',include(router.urls)),
]
