from django.db import models
from account.models import Staff, Student
from academics.models import CourseRegistration

from academics.models import Course


# Create your models here.

class Result(models.Model):
    registration=models.OneToOneField(CourseRegistration,on_delete=models.CASCADE,related_name="result")
    score=models.DecimalField(max_digits=4,decimal_places=2,blank=False, null=False)
    grade=models.CharField(max_length=2,blank=False, null=False)
    grade_point=models.DecimalField(max_digits=3,decimal_places=2,blank=False, null=False)
    is_published=models.BooleanField(default=False)
    uploaded_by=models.ForeignKey(Staff,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)




    def __str__(self):
        return(
            f"{self.registration.student.matric_number} |"
            f"{self.registration.course.code}   |"
            f"{self.score} ({self.grade})"
        )
