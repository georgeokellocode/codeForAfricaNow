from django.contrib import admin
from . models import Courses, Content, Profile, Feedback, User

# Register your models here.


admin.site.register(Courses)
admin.site.register(Content)
admin.site.register(Profile)
admin.site.register(Feedback)
admin.site.register(User)
