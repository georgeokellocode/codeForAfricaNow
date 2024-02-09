from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.http import request
from django.contrib import admin 
from . models import Courses, Profile, Content, Feedback, User



class UserRegisterForm(UserCreationForm):
    email_or_phone = forms.CharField(max_length=255, label='Email or Phone')
    location = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('username', 'email_or_phone', 'password1', 'password2', 'location')

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        

class CoursesForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['course_name', 'description', 'course_picture', 'course_banner']
        
        
class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['content_name', 'content', 'about', 'course_name', 'thumbnail']
    

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ContentForm, self).__init__(*args, **kwargs)
        self.fields['course_name'].queryset = Courses.objects.all()


class UserFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment']
        

