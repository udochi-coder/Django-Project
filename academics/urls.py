# from django.urls import path
#
# from academics.views import create_course,update_course,get_course,delete_course
#
#
#
#
#
# urlpatterns = [
#     path('create_course/', create_course, name='create_course'),
#     path('update_course/', update_course, name='update_course'),
#     path('get_course/', get_course, name='get_course'),
#     path('delete_course/', delete_course, name='delete_course'),
#
#
# ]
#
#
# from rest_framework import routers
#
# from academics.views import CourseViewSet
# from django.urls import path, include
#
#
# router = routers.DefaultRouter()
# router.register('course', CourseViewSet,basename='course')
#
#
# urlpatterns = [
#
#
#     path('', include(router.urls)),
# ]
#
from django.urls import path,include

from rest_framework.routers import DefaultRouter
from academics import views



router = DefaultRouter()
router.register('courseRegistration',views.CourseRegistrationViewSet,basename='course_registration')





urlpatterns = [
    path('',include(router.urls)),
    path('session/',views.AcademicSessionView.as_view(),name='session'),
    path('session/<int:pk>',views.GetUpdateDeleteAcademicSessionView.as_view(),name='session_detail'),
]