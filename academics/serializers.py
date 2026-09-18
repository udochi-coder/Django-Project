from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from academics.models import Course,AcademicSession,CourseRegistration
from account.models import Student


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['code','title','credit_units','level','semester','description']

    def create(self, validated_data):
        department_id = self.context.get("department_id")
        if department_id is None:
            raise serializers.ValidationError({"department": "Department context is required."})
        return Course.objects.create(department_id=department_id, **validated_data)


class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = ['name','year','semester','start_date','end_date','is_current']


class ReadAcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields= ["name","year","start_date"]


class StudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "department",
            "matric_number",
            "email",
            "level",
            "status",
        ]

class CourseRegistrationSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(
        slug_field="code",
        queryset=Course.objects.all(),
    )
    student= StudentSerializer(read_only=True)
    session_semester=serializers.SerializerMethodField()

    class Meta:
        model = CourseRegistration
        fields = ["id","course","student","session","session_semester","registered_at"]

        read_only_fields=["id","registered_at","session_semester"]



    def get_session_semester(self,obj):
        return obj.session.get_semester_display()




    def validate(self,attrs):
        course=attrs.get("course")
        session=attrs.get("session")



        if course and session:
            if course.semester != session.semester:
                raise serializers.ValidationError(
                    {
                        "course": (
                            f"'{course.code}' is a {course.get_semester_display()} course "
                            f"but the selected session is {session.get_semester_display()}."
                        ),
                    }

                )

        student=self.context.get("student")
        if student and course and session:
            if CourseRegistration.objects.filter(
                student=student,
                course=course,
                session=session
            ).exists():
                raise serializers.ValidationError(
                    {
                        "non_field_errors": (
                            f"You are already registered for '{course.code}' in this session."
                        )
                    }
                )

        return attrs






#
# class UpdateCourseSerializer(serializers.Serializer):
#     department = serializers.IntegerField()
#     code = serializers.CharField(max_length=255, required=True)
#     title = serializers.CharField(max_length=255, required=True)
#     credit_units = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
#     level = serializers.ChoiceField(choices=LEVEL_CHOICES, default="100")
#     semester = serializers.ChoiceField(choices=SEMESTER_CHOICES, default="first")
#     description = serializers.CharField(max_length=255, required=True)
#
#
# class GetCourseSerializer(serializers.Serializer):
#     code = serializers.CharField(max_length=255,required=True)
#
# class DeleteCourseSerializer(serializers.Serializer):
#     code = serializers.CharField(max_length=255,required=True)
#
#
#
#
#
#
