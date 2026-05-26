from django.urls import path

from academics.views import create_course,update_course,get_course,delete_course





urlpatterns = [
    path('create_course/', create_course, name='create_course'),
    path('update_course/', update_course, name='update_course'),
    path('get_course/', get_course, name='get_course'),
    path('delete_course/', delete_course, name='delete_course'),


]