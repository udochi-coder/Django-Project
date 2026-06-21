from django.contrib import admin
from .models import Result

# Register your models here.

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (

        "score",
        "grade",
        "grade_point",
        "is_published",
        "uploaded_by",
        "created_at",
    )

    search_fields = (
        "uploaded_by",
        "score"
    )

