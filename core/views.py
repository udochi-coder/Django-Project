from loguru import logger

from rest_framework.response import Response
from rest_framework import status

from core.models import Department
from core.serializers import DepartmentSerializer, UpdateDepartmentSerializer, GetDepartmentSerializer, \
    DeleteDepartmentSerializer
from rest_framework.decorators import api_view



# Create your views here.
@api_view(['POST'])
def create_department(request):
    try:
        serializer = DepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data['name']
        code = serializer.validated_data['code']
        if Department.objects.filter(code=code).exists():
            logger.error(f"Department with code {code} already exists")
            return Response({"message":"department with this code already exist"}, status=status.HTTP_400_BAD_REQUEST)



        Department.objects.create(**serializer.validated_data)
        logger.info(f"department {name} created")

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error creating department {str(e)}")
        return Response({"message":"error creating department"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','PATCH'])
def update_department(request):
    try:
       serializer=UpdateDepartmentSerializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       id = serializer.validated_data['id']
       name = serializer.validated_data['name']
       if not Department.objects.filter(id=id).exists():
           logger.error(f"Department with id {id} does not exist")
           return Response({"message":"department with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)


       Department.objects.filter(id=id).update(**serializer.validated_data)
       logger.info(f"department {name} updated")
       return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error updating department {str(e)}")
        return Response({"message":"error updating department"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_department(request):
    try:
        serializer = GetDepartmentSerializer(data=request.query_params)

        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']


        if not Department.objects.filter(code=code).exists():
            logger.error(f"Department with id {code} does not exist")
            return Response({"message": "department with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)

        departments= Department.objects.get(code=code)
        serializer = DepartmentSerializer(departments)
        logger.info(f"Department {code} retrieved")
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error getting department: {str(e)}")
        return Response({"message": "error getting department"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def delete_department(request):
    try:
        serializer = DeleteDepartmentSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']

        if not Department.objects.filter(code=code).exists():
            logger.error(f"Department with code {code} does not exist")
            return Response({"message":"department with this code does not exist"}, status=status.HTTP_404_NOT_FOUND)


        Department.objects.filter(code=code).update(is_active=False)
        departments = Department.objects.get(code=code)
        serializer = DepartmentSerializer(departments)


        logger.info(f"department {code} deleted")
        return Response({"message":f"department {serializer.data}has been deleted"}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error deleting department {str(e)}")
        return Response({"message":"error deleting department"}, status=status.HTTP_400_BAD_REQUEST)

