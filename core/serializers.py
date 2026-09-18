from rest_framework import serializers


from core.constants import ROLE_CHOICES
from core.models import Department,User


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name','department_code','description']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','is_active','is_staff','role']









# class UpdateDepartmentSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length=55,required=True)
#     code = serializers.CharField(max_length=55,required=True)
#     description = serializers.CharField(max_length=55,required=True)
#
#
#
# class GetDepartmentSerializer(serializers.Serializer):
#     code = serializers.CharField(max_length=55,required=True)
#
#
# class DeleteDepartmentSerializer(serializers.Serializer):
#     code = serializers.CharField(max_length=55,required=True)
#
#
# class CreateUserSerializer(serializers.Serializer):
#     first_name = serializers.CharField(max_length=255,required=True)
#     last_name = serializers.CharField(max_length=255,required=True)
#     email = serializers.EmailField(max_length=255,required=True)
#     username = serializers.CharField(max_length=255,required=True)
#     role=serializers.ChoiceField(choices=ROLE_CHOICES,default="student")
#
#
# class GetUserSerializer(serializers.Serializer):
#     username=serializers.CharField(max_length=255,required=True)
#
# class DeleteUserSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=255,required=True)
#
#
#
#
#
#
#
#
#
#
#
