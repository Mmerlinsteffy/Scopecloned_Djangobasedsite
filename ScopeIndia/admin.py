from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(Maincourse)
admin.site.register(Subcourse)
admin.site.register(CourseContent)
admin.site.register(Registration)
admin.site.register(StudentLogin)