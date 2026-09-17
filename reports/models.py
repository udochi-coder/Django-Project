from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from account.models import Student
from academics.models import AcademicSession,CourseRegistration
from results.models import Result


# Create your models here.

class SemesterReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="semester_report")
    session = models.ForeignKey(AcademicSession, on_delete=models.PROTECT, related_name="semester_report")
    total_units = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(80)])
    total_grade_point = models.DecimalField(max_digits=6,decimal_places=4,blank=False, null=False)
    semester_gpa = models.DecimalField(max_digits=6,decimal_places=4,blank=False, null=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def calculate_semester_gpa(self):
        registration = CourseRegistration.objects.filter(
            semester=self.session,
            student=self.student,
        ).select_related("semester","course")

        total_units = 0
        total_point = 0



        for reg in registration:
            result = getattr(reg, 'result' ,None)
            if result and result.is_published:
                units= reg.course.units
                total_units += units
                total_point += units * result.grade_point
                






    def __str__(self):
        return(
            f"{self.student.matric_number} |"
            f"{self.session.semester} |"


        )


