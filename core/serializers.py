from rest_framework import serializers



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




