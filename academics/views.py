# from loguru import logger
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from academics.models import Course
# from academics.serializers import CourseSerializer, UpdateCourseSerializer, GetCourseSerializer, DeleteCourseSerializer
#
#
# # Create your views here.
#
# @api_view(['POST'])
# def create_course(request):
#     try:
#         serializer = CourseSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         title = serializer.validated_data['title']
#         code = serializer.validated_data['code']
#         if Course.objects.filter(code=code).exists():
#             logger.error(f"Course {code} already exists")
#             return Response({"message": "Course with this code already exist"}, status=status.HTTP_400_BAD_REQUEST)
#
#         Course.objects.create(**serializer.validated_data)
#         logger.error(f"Course {title} created")
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
#     except Exception as e:
#         logger.error(f"Error creating Course {str(e)}")
#         return Response({"message": "Error creating Course"}, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['PUT','PATCH'])
# def update_course(request):
#     try:
#         serializer = UpdateCourseSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         code = serializer.validated_data['code']
#
#         if not Course.objects.filter(code=code).exists():
#             logger.error(f"Course with id {code} does not exist")
#             return Response({"message": "Course with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
#
#         Course.objects.filter(code=code).update(**serializer.validated_data)
#         logger.error(f"Course {code} updated")
#         return Response({"message": "Course updated successfully"}, status=status.HTTP_200_OK)
#     except Exception as e:
#         logger.error(f"Error updating Course {str(e)}")
#         return Response({"message": "Error updating Course"}, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['GET'])
# def get_course(request):
#     try:
#         serializer = GetCourseSerializer(data=request.query_params)
#         serializer.is_valid(raise_exception=True)
#
#         code = serializer.validated_data['code']
#
#         if not Course.objects.filter(code=code).exists():
#             logger.error(f"Course {code} does not exist")
#             return Response({"message": "Course with this code does not exist"}, status=status.HTTP_404_NOT_FOUND)
#
#
#         courses = Course.objects.get(code=code)
#         serializer = CourseSerializer(courses)
#         logger.info(f"Course {code} retrieved")
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         logger.error(f"Error retrieving Course {str(e)}")
#         return Response({"message": "Error retrieving Course"}, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['DELETE'])
# def delete_course(request):
#     try:
#         serializer = DeleteCourseSerializer(data=request.query_params)
#         serializer.is_valid(raise_exception=True)
#         code = serializer.validated_data['code']
#
#         if not Course.objects.filter(code=code).exists():
#             logger.error(f"Course {code} does not exist")
#             return Response({"message": "Course with this code does not exist"}, status=status.HTTP_404_NOT_FOUND)
#
#         Course.objects.filter(code=code).update(is_active=False)
#         courses=Course.objects.get(code=code)
#         serializers=CourseSerializer(courses)
#
#         logger.info(f"Course {code} deleted")
#         return Response({"message": f"Course {serializers.data} has been successfully deleted"}, status=status.HTTP_200_OK)
#     except Exception as e:
#         logger.error(f"Error deleting Course {str(e)}")
#         return Response({"message": "Error deleting Course"}, status=status.HTTP_400_BAD_REQUEST)
#
from loguru import logger

from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from academics.models import Course,AcademicSession,CourseRegistration
from academics.serializers import CourseSerializer, AcademicSessionSerializer, CourseRegistrationSerializer, \
    ReadAcademicSessionSerializer
from core.constants import ROLE_STUDENT
from account.models import Student
from core.models import User


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        department_id = self.kwargs.get("department_pk")
        return Course.objects.filter(department_id=department_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["department_id"] = self.kwargs.get("department_pk")
        return context

class AcademicSessionView(ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AcademicSessionSerializer
        return ReadAcademicSessionSerializer

class GetUpdateDeleteAcademicSessionView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer

class CourseRegistrationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = CourseRegistrationSerializer

    def get_queryset(self):
        user = self.request.user
        qs = CourseRegistration.objects.select_related(
            "student__user", "course__department", "session"
        ).all()

        if getattr(user, "role", None) != ROLE_STUDENT:
            return qs.none()

        student = getattr(user, "student_profile", None)
        if student is None or student.status != "active":
            return qs.none()

        qs = qs.filter(student=student)

        return qs


    def get_serializer_context(self):
        context=super().get_serializer_context()
        user = self.request.user


        if user.is_authenticated and getattr(user, "role", None) == ROLE_STUDENT:
            student = getattr(user, "student_profile", None)
            if student is not None and student.status == "active":
                context["student"] = student


        return context


    def create(self,request,*args,**kwargs):
        if getattr(request.user, "role", None) != ROLE_STUDENT:
            logger.warning(
                f"Non-student user_id={request.user.id} attempted course registration"
            )
            return Response(
                {"error":"Only students can register for courses."},
                status=status.HTTP_403_FORBIDDEN,

            )
        try:
            student = request.user.student_profile
        except Exception:
            logger.error(
                f"User id={request.user.id} has role=student but no student profile"
            )
            return Response(
                {"error":"No student profile found for this account. Contact admin."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if student.status != "active":
            return Response(
                {"error": "Only active students can register for courses."},
                status=status.HTTP_403_FORBIDDEN,
            )
        logger.info(
            f"Course registration attempt - "
            f"student={student.matric_number}, "
            f"payload={request.data}"
        )

        serializer = self.get_serializer(data=request.data)

        try:
            if not serializer.is_valid():
                logger.warning(
            f"Registration failed  - student={student.matric_number}, "
            f"errors={serializer.errors}"
                )
                return Response(
                    {"errors":serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            registration = serializer.save(student=student)

            logger.success(
            f"Registration created - id= {registration.id}, "
            f"student={student.matric_number}, "
            f"course={registration.course.code}, "
            f"session={registration.session.name}, "
            )
            return Response(
            self.get_serializer(registration).data,
            status=status.HTTP_201_CREATED,

            )
        except IntegrityError as e:
            logger.error(
                f"Duplicate registration (race condition) - "
                f"student={student.matric_number}, "
                f"data={request.data}"
            )
            return Response(
                {"error":" You are already registered for  this course in the selected session."},
                status=status.HTTP_409_CONFLICT,
            )
        except Exception as exc:
            logger.exception(f"Unexpected error during registration: {exc}")
            return Response(
                {"error": "An unexpected error occured . Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


    def destroy(self,request,*args,**kwargs):
        registration = self.get_object()
        student = getattr(request.user, "student_profile", None)

        if getattr(request.user, "role", None) != ROLE_STUDENT:
            return Response(
                {"error": "Only students can drop course registrations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if student is None:
            return Response(
                {"error": "No student profile found for this account."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if student.status != "active":
            return Response(
                {"error": "Only active students can drop course registrations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if registration.student != student:
            logger.warning(
                f"Student {request.user.id} attempted to drop"
                f"another student's registration id= {registration.id}"
            )
            return Response(
                {"error":"You can only drop your own course registrations. "},
                status=status.HTTP_403_FORBIDDEN,
            )

        logger.info(
            f"Dropping registration id= {registration.id} -"
            f"student={registration.student.matric_number}, "
            f"course={registration.course.code}, "
        )

        registration.delete()
        logger.success(f"Registration id= {registration.id} dropped successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)




