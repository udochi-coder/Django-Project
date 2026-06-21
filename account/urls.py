from django.urls import path



from . import views





urlpatterns = [

    path('student_enroll/',views.StudentEnrollment.as_view(),name='student_enroll'),
    path('staff_register/',views.StaffRegistration.as_view(),name='staff_register'),
    path('auth/login',views.LoginView.as_view(),name='login'),
]


# {
#   "department": "CSC",
#   "level": "100",
#   "entry_year": 2026,
#   "email": "student@example.com",
#   "username": "student1",
#   "password": "StrongPass123!",
#   "first_name": "Ada",
#   "last_name": "Nwosu"
# }
