from django.contrib import admin
from .models import Course, AcademicSession, CourseRegistration


# Register your models here.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code","department","credit_units","level","semester","created_at")
    search_fields = ("code","credit_units","semester")

@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ("name","year","semester","start_date","end_date")
    search_fields = ("name","year","semester")

@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ("course","student","session")
    search_fields = ("course","student","session")