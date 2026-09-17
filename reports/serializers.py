from academics.models import CourseRegistration
from account.models import Student
from reports.models import SemesterReport
from rest_framework import serializers
from academics.serializers import StudentSerializer


class ReportSerializer(serializers.ModelSerializer):

    matric_number = serializers.CharField(write_only=True)


    student= StudentSerializer(read_only=True)
    session_semester = serializers.SerializerMethodField()

    class Meta:
        model = SemesterReport
        fields = [
            "id",
            "matric_number",
            "session"
            "session_semester",
            "total_units",
            "total_grade_point",
            "semester_gpa",
            "is_published",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "student"
            "session_semester",
            "total_units",
            "total_grade_point",
            "semester_gpa",
            "is_published",
            "created_at",
            "updated_at",
        ]


    def get_session_semester(self, obj):
        return obj.session.get_semester_display()



    def validate(self, attrs):
        session = attrs.get("session")
        student = self.context.get("student")


        if session and student:
            if SemesterReport.objects.filter(
                session=session,
                student=student,
            ).exists():
                raise serializers.ValidationError(
                    {
                        "non_field_errors": (
                            f"This semester report for '{student.matric_number}' has already been published."

                        )
                    }
                )
        return attrs








