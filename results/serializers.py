from decimal import Decimal
from results.models import Result, CourseRegistration
from rest_framework import serializers


class ResultSerializer(serializers.ModelSerializer):

    matric_number = serializers.CharField(write_only=True)
    course = serializers.CharField(write_only=True, help_text="Course code")


    course_code = serializers.CharField(source="registration.course.code", read_only=True)
    course_title = serializers.CharField(source="registration.course.title", read_only=True)
    credit_units = serializers.IntegerField(source="registration.course.credit_units", read_only=True)

    class Meta:
        model = Result
        fields = [
            "id",
            "matric_number",
            "course",
            "course_code",
            "course_title",
            "credit_units",
            "score",
            "grade",
            "grade_point",
            "is_published",
            "uploaded_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "registration",
            "grade",
            "grade_point",
            "uploaded_by",
            "created_at",
            "updated_at",
        ]

    def validate_score(self, marks):
        if marks < 0 or marks > 100:
            raise serializers.ValidationError("Score must be between 0 and 100.")
        return marks

    def get_grade_and_grade_point(self, score):
        if score >= 70:
            return "A", Decimal("5.0")
        if score >= 60:
            return "B", Decimal("4.0")
        if score >= 50:
            return "C", Decimal("3.0")
        if score >= 45:
            return "D", Decimal("2.0")
        if score >= 40:
            return "E", Decimal("1.0")
        return "F", Decimal("0.0")

    def validate(self, attrs):
        matric_number = attrs.pop("matric_number")
        course_code = attrs.pop("course")

        try:
            registration = CourseRegistration.objects.get(
                student__matric_number=matric_number,
                course__code=course_code,
            )
        except CourseRegistration.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "matric_number": (
                        f"No registration found for '{matric_number}' in course '{course_code}'."
                    )
                }
            )
        except CourseRegistration.MultipleObjectsReturned:
            raise serializers.ValidationError(
                {
                    "matric_number": (
                        f"Multiple registrations found for '{matric_number}' in '{course_code}'. "
                        f"Contact admin to disambiguate by session."
                    )
                }
            )

        attrs["registration"] = registration

        marks = attrs["score"]
        grade, grade_point = self.get_grade_and_grade_point(score=marks)
        attrs["grade"] = grade
        attrs["grade_point"] = grade_point

        return attrs



#
# def calculate_each_semester_gpa(self, student):
#     registrations = CourseRegistration.objects.filter(student=student)
#     semester_gpas = {}
#
#     for reg in registrations:
#         course_results = Result.objects.filter(course_registration=reg)
#
#         if course_results.exists():
#             semester=reg.session.semester
#
#             if semester not in semester_gpas:
#                 semester_gpas[semester]={"points": 0, "units": 0}
#
#                 total_points = sum(result.grade_point * reg.course.credit_units for result in course_results)
#                 total_units = sum(result.registration.course.credit_units for result in course_results)
#
#
#                 semester_gpas[semester]["points"] += total_points
#                 semester_gpas[semester]["units"] += total_units
#
#
#     for semester in semester_gpas:
#         data=semester_gpas[semester]
#         semester_gpas[semester] = data["points"]/data["units"]
#
#     return semester_gpas




























    
    






# class CourseRegistrationSerializer(serializers.ModelSerializer):
#     course = serializers.SlugRelatedField(
#         slug_field="code",
#         queryset=Course.objects.all(),
#     )
#     student= StudentSerializer(read_only=True)
#     session_semester=serializers.SerializerMethodField()
#
#     class Meta:
#         model = CourseRegistration
#         fields = ["id","course","student","session","session_semester","registered_at"]
#
#         read_only_fields=["id","registered_at","session_semester"]
#
#
#
#     def get_session_semester(self,obj):
#         return obj.session.get_semester_display()
#
#
#
#
#     def validate(self,attrs):
#         course=attrs.get("course")
#         session=attrs.get("session")
#
#
#
#         if course and session:
#             if course.semester != session.semester:
#                 raise serializers.ValidationError(
#                     {
#                         "course": (
#                             f"'{course.code}' is a {course.get_semester_display()} course "
#                             f"but the selected session is {session.get_semester_display()}."
#                         ),
#                     }
#
#                 )
#
#         student=self.context.get("student")
#         if student and course and session:
#             if CourseRegistration.objects.filter(
#                 student=student,
#                 course=course,
#                 session=session
#             ).exists():
#                 raise serializers.ValidationError(
#                     {
#                         "non_field_errors": (
#                             f"You are already registered for '{course.code}' in this session."
#                         )
#                     }
#                 )
#
#         return attrs
