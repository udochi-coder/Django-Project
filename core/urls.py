from core.views import *
from django.urls import path




urlpatterns = [
    path('create_department/', create_department, name='create_department'),
    path('update_department/', update_department, name='update_department'),
    path('get_department/', get_department, name='get_department'),
    path('delete_department/', delete_department, name='delete_department'),
    path('create_user/', create_user, name='create_user'),
    path('update_user/', update_user, name='update_user'),
    path('get_user/', get_user, name='get_user'),
    path('delete_user/', delete_user, name='delete_user'),


]
