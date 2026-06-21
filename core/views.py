# from loguru import logger
from django.core.mail import send_mail
from loguru import logger
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
# from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from core.models import Department, User
from core.serializers import *
# from rest_framework.decorators import api_view
#
#
#
#
# # Create your views here.
# @api_view(['POST'])
# def create_department(request):
#     try:
#         serializer = DepartmentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         name = serializer.validated_data['name']
#         code = serializer.validated_data['code']
#         if Department.objects.filter(code=code).exists():
#             logger.error(f"Department with code {code} already exists")
#             return Response({"message":"department with this code already exist"}, status=status.HTTP_400_BAD_REQUEST)
#
#
#
#         Department.objects.create(**serializer.validated_data)
#         logger.info(f"department {name} created")
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     except Exception as e:
#         logger.error(f"Error creating department {str(e)}")
#         return Response({"message":"error creating department"}, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['PUT','PATCH'])
# def update_department(request):
#     try:
#        serializer=UpdateDepartmentSerializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        id = serializer.validated_data['id']
#        name = serializer.validated_data['name']
#        if not Department.objects.filter(id=id).exists():
#            logger.error(f"Department with id {id} does not exist")
#            return Response({"message":"department with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
#
#
#        Department.objects.filter(id=id).update(**serializer.validated_data)
#        logger.info(f"department {name} updated")
#        return Response(serializer.data, status=status.HTTP_200_OK)
#
#     except Exception as e:
#         logger.error(f"Error updating department {str(e)}")
#         return Response({"message":"error updating department"}, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET'])
# def get_department(request):
#     try:
#         serializer = GetDepartmentSerializer(data=request.query_params)
#
#         serializer.is_valid(raise_exception=True)
#
#         code = serializer.validated_data['code']
#
#
#         if not Department.objects.filter(code=code).exists():
#             logger.error(f"Department with id {code} does not exist")
#             return Response({"message": "department with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
#
#         departments= Department.objects.get(code=code)
#         serializer = DepartmentSerializer(departments)
#         logger.info(f"Department {code} retrieved")
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     except Exception as e:
#         logger.error(f"Error getting department: {str(e)}")
#         return Response({"message": "error getting department"}, status=status.HTTP_400_BAD_REQUEST)
#
#
#
# @api_view(['DELETE'])
# def delete_department(request):
#     try:
#         serializer = DeleteDepartmentSerializer(data=request.query_params)
#         serializer.is_valid(raise_exception=True)
#         code = serializer.validated_data['code']
#
#         if not Department.objects.filter(code=code).exists():
#             logger.error(f"Department with code {code} does not exist")
#             return Response({"message":"department with this code does not exist"}, status=status.HTTP_404_NOT_FOUND)
#
#
#         Department.objects.filter(code=code).update(is_active=False)
#         departments = Department.objects.get(code=code)
#         serializer = DepartmentSerializer(departments)
#
#
#         logger.info(f"department {code} deleted")
#         return Response({"message":f"department {serializer.data}has been deleted"}, status=status.HTTP_200_OK)
#
#     except Exception as e:
#         logger.error(f"Error deleting department {str(e)}")
#         return Response({"message":"error deleting department"}, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['POST'])
# def create_user(request):
#     try:
#         serializer = CreateUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.validated_data['username']
#         email=serializer.validated_data['email']
#
#
#         if User.objects.filter(username=username).exists():
#             logger.error(f"User with username {username} already exists")
#             return Response({"message":"user with username already exists"}, status=status.HTTP_400_BAD_REQUEST)
#
#
#         User.objects.create(**serializer.validated_data)
#         logger.info(f"user with username {username}  and {email} created")
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     except Exception as e:
#         logger.error(f"Error creating user {str(e)}")
#         return Response({"message":"error creating user"}, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['PUT','PATCH'])
# def update_user(request):
#     try:
#         serializer=CreateUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.validated_data['username']
#
#         if not User.objects.filter(username=username).exists():
#             logger.error(f"User with username {username} does not exist")
#             return Response({"message":"user with username does not exist"}, status=status.HTTP_404_NOT_FOUND)
#
#
#
#         User.objects.filter(username=username).update(**serializer.validated_data)
#         logger.info(f"user with username {username} updated")
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     except Exception as e:
#         logger.error(f"Error updating user {str(e)}")
#         return Response({"message":"error updating user"}, status=status.HTTP_400_BAD_REQUEST)
#
#
#
# @api_view(['GET'])
# def get_user(request):
#     try:
#         serializer = GetUserSerializer(data=request.query_params)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.validated_data['username']
#
#         if not User.objects.filter(username=username).exists():
#             logger.error(f"User with username {username} does not exist")
#             return Response({"message":"user with username does not exist"}, status=status.HTTP_404_NOT_FOUND)
#
#
#
#         user=User.objects.get(username=username)
#         serializers=CreateUserSerializer(user)
#
#         return Response(serializers.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         logger.error(f"Error getting user {str(e)}")
#         return Response({"message":"error getting user"}, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['DELETE'])
# def delete_user(request):
#     try:
#         serializer=DeleteUserSerializer(data=request.query_params)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.validated_data['username']
#
#         if not User.objects.filter(username=username).exists():
#             logger.error(f"User with username {username} does not exist")
#             return Response({"message":"user with username does not exist"}, status=status.HTTP_404_NOT_FOUND)
#
#
#         User.objects.filter(username=username).update(is_active=False)
#
#         logger.info(f"user with username {username} deleted")
#         return Response({"message":f"user with {username} has been deleted"}, status=status.HTTP_200_OK)
#
#     except Exception as e:
#         logger.error(f"Error deleting user {str(e)}")
#         return Response({"message":"error deleting user"}, status=status.HTTP_400_BAD_REQUEST)
#
#
class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

class UserViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer



@api_view(['POST'])
def send_message(request):
    message = request.data.get('message')
    email = request.data.get('email')
    subject = request.data.get('subject')

    try:
        send_mail(subject=subject, message=message, from_email="no-reply@resultportal.com", recipient_list=[email,])
        logger.info(f"Message sent to {email}")
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"message": "Mail sent successfully"},status=status.HTTP_200_OK)


