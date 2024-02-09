from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', LoginView.as_view(next_page='courses'), name='login'),
    path('register/', views.register, name='register'),
    path('play_video/<int:pk>', views.play_video, name='play_video'),
    path('profile/', views.profile, name='UserProfile'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('', views.index, name="index"),
    path('create_course/', views.create_course, name="create_course"),
    path('course_details/<int:pk>', views.course_details, name="course_details"),
    path('courses/', views.courses, name="courses"),
    path('create_child/', views.create_child, name="create_child"),
    path('create_instructor/', views.create_instructor, name="create_instructor"),
    path('upload/', views.upload, name='upload'),
    path('post_user_feedback/', views.post_user_feedback, name='post_user_feedback'),
    path('get_user_feedback/', views.get_user_feedback, name='get_user_feedback'),
]
