from loguru import logger
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from academics.models import Course
from academics.serializers import CourseSerializer,UpdateCourseSerializer






# Create your views here.

@api_view(['POST'])
def create_course(request):
    try:
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data['title']
        code = serializer.validated_data['code']
        if Course.objects.filter(code=code).exists():
            logger.error(f"Course {code} already exists")
            return Response({"message": "Course with this code already exist"}, status=status.HTTP_400_BAD_REQUEST)

        Course.objects.create(**serializer.validated_data)
        logger.error(f"Course {title} created")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    except Exception as e:
        logger.error(f"Error creating Course {str(e)}")
        return Response({"message": "Error creating Course"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','PATCH'])
def update_course(request):
    try:
        serializer = UpdateCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']

        if not Course.objects.filter(code=code).exists():
            logger.error(f"Course with id {code} does not exist")
            return Response({"message": "Course with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)

        Course.objects.filter(code=code).update(**serializer.validated_data)
        logger.error(f"Course {code} updated")
        return Response({"message": "Course updated successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error updating Course {str(e)}")
        return Response({"message": "Error updating Course"}, status=status.HTTP_400_BAD_REQUEST)

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
