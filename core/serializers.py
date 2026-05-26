from rest_framework import serializers


from core.constants import ROLE_CHOICES


class DepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=55,required=True)
    code = serializers.CharField(max_length=55,required=True)
    description=serializers.CharField(max_length=55,required=True)


class UpdateDepartmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=55,required=True)
    code = serializers.CharField(max_length=55,required=True)
    description = serializers.CharField(max_length=55,required=True)



class GetDepartmentSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=55,required=True)


class DeleteDepartmentSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=55,required=True)


class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255,required=True)
    last_name = serializers.CharField(max_length=255,required=True)
    email = serializers.EmailField(max_length=255,required=True)
    username = serializers.CharField(max_length=255,required=True)
    role=serializers.ChoiceField(choices=ROLE_CHOICES,default="student")


class GetUserSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=255,required=True)

class DeleteUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255,required=True)





