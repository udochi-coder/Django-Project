from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.constants import LEVEL_CHOICES, SEMESTER_CHOICES
from core.models import Department
from core.serializers import DepartmentSerializer


class CourseSerializer(serializers.Serializer):
    department=serializers.PrimaryKeyRelatedField(queryset=Department.objects.filter(is_active=True))
    code = serializers.CharField(max_length=255,required=True)
    title = serializers.CharField(max_length=255,required=True)
    credit_units = serializers.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(6)])
    level = serializers.ChoiceField(choices=LEVEL_CHOICES, default="100")
    semester = serializers.ChoiceField(choices=SEMESTER_CHOICES, default="first")
    description = serializers.CharField(max_length=255, required=True)




class UpdateCourseSerializer(serializers.Serializer):
    department = serializers.IntegerField()
    code = serializers.CharField(max_length=255, required=True)
    title = serializers.CharField(max_length=255, required=True)
    credit_units = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    level = serializers.ChoiceField(choices=LEVEL_CHOICES, default="100")
    semester = serializers.ChoiceField(choices=SEMESTER_CHOICES, default="first")
    description = serializers.CharField(max_length=255, required=True)


class GetCourseSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=255,required=True)

class DeleteCourseSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=255,required=True)






