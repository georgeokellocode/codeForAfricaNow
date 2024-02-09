# from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from . models import Courses, Content, Feedback, User
from . forms import CoursesForm, ContentForm, UserFeedbackForm
from django.contrib.auth.decorators import user_passes_test
# from moviepy.editor import *

# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.is_staff and user.is_superuser



def index(request):
    return render(request, "index.html")


def courses(request):
    courses = Courses.objects.all()
    return render(request, 'courses.html', {'courses':courses})

@login_required(login_url='/login/')
def course_details(request, pk):
    course = get_object_or_404(Courses, pk=pk)
    course_name = course.id
    contents = Content.objects.filter(course_name=course_name)
    #subscribers = channel.subscribers.count()
    pk = pk
    return render(request, 'course_details.html', {'course':course, 'contents':contents, })


@user_passes_test(is_admin)
def create_course(request):
    if request.method == 'POST':
        c_form = CoursesForm(request.POST, request.FILES)
        if c_form.is_valid():
            course_name = c_form.cleaned_data['course_name']
            description = c_form.cleaned_data['description']
            course_picture = c_form.cleaned_data['course_picture']
            course_banner = c_form.cleaned_data['course_banner']

            Courses.objects.create(
                course_name = course_name,
                user = request.user,
                description = description,
                course_picture = course_picture,
                course_banner = course_banner
            )
            return redirect('courses')
    else:
        c_form = CoursesForm()
    return render(request, 'create_course.html', {'c_form': c_form})

@login_required(login_url='/login/')
def create_child(request):
    return render(request, "create_child.html")


def create_instructor(request):
    return render(request, "create_instructor.html")


# def login(request):
#     return render(request, "courses.html")


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            messages.error(request, 'An error occurred while processing your request.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register2.html', {'forms': form})



@login_required(login_url=("login"))
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            
            data={
            'error': False, 
            'message': 'Uploaded Successfully'
            }
            return JsonResponse(data, safe=False)
            # messages.success(request, f'Your account has been updated!')
            # return redirect('Home')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)
    


def forgot_password(request):
    return render(request,'registration/forgot_password.html')


@login_required(login_url=("login"))
def upload(request):   
    if request.method == 'POST':
        form = ContentForm(request.user,request.POST, request.FILES,)
        if form.is_valid():
            obj = form.save()
            # print(request.FILES)
            # vid = request.FILES('id_content')[0]
            #clip = VideoFileClip(vid.temporary_file_path())
            #obj.duration = clip.duration
            print()
            #obj.save(clip.duration)
            data={
            'error': False, 
            'message': 'Uploaded Successfully'
            }
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'error': True, 'errors': 'Error occured'})
    else:
        form = ContentForm(request.user)
    return render(request, 'upload.html', {'form': form})



@login_required(login_url=("login"))
def play_video(request, pk):
    content = get_object_or_404(Content, pk=pk)
    course_name = content.course_name
    contents = Content.objects.filter(course_name=course_name)
    
    # pk = pk
    
    # ip = request.META['REMOTE_ADDR']
    # if not VideoViews.objects.filter(video=video, session=request.session.session_key):
    #     view = VideoViews(video=video, ip_addr=ip, session=request.session.session_key)
    #     view.save()
    # video_views = VideoViews.objects.filter(video=video).count()
    # subscribers_count = video.channel_name.subscribers.count()
    context = {
        'content':content, 
        'contents':contents, 
    }

    return render(request, 'content-page.html', context)


def get_user_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-date')
    context = {
        'feedbacks': feedbacks,
    }
    return render(request, 'userFeedback.html', context)


def post_user_feedback(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        contentCommented = request.POST['contentComment']
        Feedback.objects.create(
            comment = comment,
            contentCommented = contentCommented,
        )
        messages.success(request, f'Your account has been created! You are now able to log in')
    messages.error(request, 'An error occurred while processing your request.')
    return HttpResponse('')

