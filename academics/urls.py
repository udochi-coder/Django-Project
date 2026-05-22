from django.urls import path

from academics.views import create_course,update_course





urlpatterns = [
    path('create_course/', create_course, name='create_course'),
    path('update_course/', update_course, name='update_course'),


]