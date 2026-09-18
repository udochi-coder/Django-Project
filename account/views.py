from django.db import transaction
from loguru import logger
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from account.models import Staff, Student
from account.serializers import StaffRegistrationSerializer, StudentEnrollmentSerializer, CustomTokenObtainSerializer
from core.models import Department, User


class StudentEnrollment(APIView):

    def post(self, request, *args, **kwargs):

        try:
            serializer = StudentEnrollmentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            department_code = serializer.validated_data["department"]
            department = Department.objects.filter(department_code=department_code).first()
            if department is None:
                return Response({"message": "Department does not exist"}, status=status.HTTP_404_NOT_FOUND)


            with transaction.atomic():
                user = User(
                    username=serializer.validated_data["username"],
                    email=serializer.validated_data["email"],
                    first_name=serializer.validated_data["first_name"],
                    last_name=serializer.validated_data["last_name"],
                    role="student",

                )
                user.set_password(serializer.validated_data["password"])
                user.save()

                student = Student.objects.create(
                    user=user,
                    department=department,
                    level=serializer.validated_data.get("level", "100"),
                    entry_year=serializer.validated_data["entry_year"],
                )
                student.save()
                logger.info(f"Student has been successfully enrolled ")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating Student {str(e)}")
            return Response({"message": "Error enrolling Student"}, status=status.HTTP_400_BAD_REQUEST)




class StaffRegistration(APIView):
    def post(self, request, *args, **kwargs):


        try:
            serializer = StaffRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            department_code = serializer.validated_data["department"]
            department = Department.objects.filter(department_code=department_code).first()
            if department is None:
                return Response({"message": "Department does not exist"}, status=status.HTTP_404_NOT_FOUND)


            with transaction.atomic():
                user = User(
                    username=serializer.validated_data["username"],
                    email=serializer.validated_data["email"],
                    first_name=serializer.validated_data["first_name"],
                    last_name=serializer.validated_data["last_name"],
                    role="staff",

                )
                user.set_password(serializer.validated_data["password"])
                user.save()

                staff=Staff.objects.create(
                    user=user,
                    department=department,

                )
                staff.save()

                logger.info(f"Staff has been successfully registered")
                return Response(serializer.data, status=status.HTTP_201_CREATED)



        except Exception as e:
            logger.error(f"Error enrolling Staff {str(e)}")
            return Response({"message": "Error  Staff"}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainSerializer

    def post(self,request,*args,**kwargs):
        user_email = request.data.get("email")
        logger.info(f"User {user_email} is attempting to login")
        serializer = self.serializer_class(data=request.data)
        try:


            serializer.is_valid(raise_exception=True)

        except TokenError as e:
            logger.info(f"Invalid token:{e}")
            return Response(
                {"message": "We couldn't sign you in. Please check the demo account instead."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except serializers.ValidationError as e:
            logger.info(f"Login rejected for {user_email}: {e}")
            detail = e.detail
            message = detail.get("non_field_errors", [str(e)])[0] if isinstance(detail, dict) else str(e)
            return Response({"message": str(message)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"An error occurred while login in for:{e}")
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"User{user_email} logged in successfully")
        return Response(serializer.validated_data,status=status.HTTP_200_OK)
