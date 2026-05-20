from typing import Required
from django.db import models
from django.db.models.base import CASCADE

# Create your models here.
class Maincourse(models.Model):
    maincourse_name=models.CharField(max_length=90)
    def __str__(self):
        return self.maincourse_name
class Subcourse(models.Model):
    subcourse_name=models.CharField(max_length=90)
    maincourse_name=models.ForeignKey(Maincourse,on_delete=CASCADE,null=True)
    course_title=models.CharField(null=True,max_length=90)
    Course_duration=models.CharField(null=True,max_length=90)
    course_timing=models.CharField(null=True,max_length=90)
    next_batch=models.DateField(null=True)
    def __str__(self):
        return self.subcourse_name
class CourseContent(models.Model):
    subcourse = models.ForeignKey(Subcourse, on_delete=models.CASCADE, related_name="contents",null=True)
    title = models.CharField(max_length=150,blank=True)
    def __str__(self):
        return self.title
class Registration(models.Model):
    fullname = models.CharField(max_length=90, blank=False)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=34, blank=False)
    eduqual = models.CharField(max_length=90, null=True, blank=True)
    mobile = models.CharField(max_length=15, blank=False)
    email = models.EmailField(max_length=254, blank=False, unique=True)
    guardname = models.CharField(max_length=90, null=True, blank=True)
    guard_occu = models.CharField(max_length=90, null=True, blank=True)
    guard_mob = models.CharField(max_length=15, null=True, blank=True)
    course = models.CharField(max_length=90, blank=False)
    train_mode = models.CharField(max_length=90, null=True, blank=True)
    location = models.CharField(max_length=90, null=True, blank=True)
    timing = models.TextField(null=True, blank=True) 
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=90, null=True, blank=True)
    state = models.CharField(max_length=90, null=True, blank=True)
    city = models.CharField(max_length=90, null=True, blank=True)
    pin = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.fullname
class StudentLogin(models.Model):
    student_id=models.OneToOneField(Registration,on_delete=models.CASCADE )
    username=models.EmailField(unique=True)
    password=models.CharField(max_length=255,null=False)
    file=models.FileField(upload_to='Images/',null=True)
    def __str__(self):
        return self.username