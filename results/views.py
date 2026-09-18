from django.db import IntegrityError
from django.shortcuts import render
from loguru import logger
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, SAFE_METHODS

from account.models import Staff
from core.constants import ROLE_STAFF, ROLE_STUDENT
from results.models import Result
from results.serializers import ResultSerializer
# Create your views here.

class IsStudentCanReadStaffCanWrite(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        role = getattr(user, "role", None)

        if request.method in SAFE_METHODS:
            return role in (ROLE_STUDENT, ROLE_STAFF)

        return role == ROLE_STAFF


class ResultViewSet(ModelViewSet):
    permission_classes = [IsStudentCanReadStaffCanWrite]

    serializer_class = ResultSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Result.objects.select_related(
            "registration__course", "registration__student"
        ).all()

        if getattr(user, "role", None) == ROLE_STAFF:
            return qs

        if getattr(user, "role", None) == ROLE_STUDENT:
            student = getattr(user, "student_profile", None)
            if student and student.status == "active":
                return qs.filter(registration__student=student)

        return qs.none()

    def create(self, request, *args, **kwargs):
        if getattr(request.user, "role", None) != ROLE_STAFF:
            logger.warning(
                f"Non staff user_id={request.user.id} attempted to upload a result"
            )
            return Response(
                {"error": "Only staff can upload results"},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            staff = request.user.staff
        except Staff.DoesNotExist:
            logger.error(
                f"User id={request.user.id} has role=staff but no staff profile"
            )
            return Response(
                {"error": "No staff profile for this account. Contact admin"},
                status=status.HTTP_400_BAD_REQUEST,
            )



        serializer = self.get_serializer(data=request.data)

        try:
            if not serializer.is_valid():
                logger.warning(
                    f"Upload failed - staff={staff.department}, "
                    f"errors={serializer.errors}"
                )
                return Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            upload = serializer.save(uploaded_by=staff)

            logger.success(
                f"Result upload created - id={upload.id}, "
                f"score={upload.score}, "
                f"grade={upload.grade}, "
                f"grade_point={upload.grade_point}"
            )
            return Response(
                self.get_serializer(upload).data,
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError:
            logger.error(
                f"Duplicate upload (race condition) - "
                f"staff={staff.department}, data={request.data}"
            )
            return Response(
                {"errors": "You have already uploaded this result"},
                status=status.HTTP_409_CONFLICT,
            )
        except Exception as exception:
            logger.exception(f"Unexpected error during upload: {exception}")
            return Response(
                {"error": "An unexpected error occurred. Please try again later or contact admin"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        upload = self.get_object()
        staff = getattr(request.user, "staff", None)

        if getattr(request.user, "role", None) != ROLE_STAFF:
            return Response(
                {"error": "Only staff can attempt to delete results"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if staff is None:
            return Response(
                {"error": "No staff profile for this account. Contact admin"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if upload.staff != staff:
            logger.warning(
                f"Staff {request.user.id} attempted to delete result "
                f"that was  uploaded by id={upload.id} "
            )
            return Response(
                {"error":"You can only delete a result you uploaded yourself"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if upload.is_published:
            raise PermissionDenied("Cannot delete a published result. Contact admin")
        return super().destroy(request, *args, **kwargs)