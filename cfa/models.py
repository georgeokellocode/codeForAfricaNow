from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.files.storage import default_storage as storage



# Create your models here.

class User(AbstractUser):
    location = models.CharField(max_length=255, blank=True, null=True)

class Courses(models.Model):
    course_name = models.CharField(max_length=120)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='course_user')
    description = models.TextField()
    course_picture = models.ImageField(default="default.jpg", null=True, blank=True, upload_to='course_pics')
    course_banner = models.ImageField( default="default.jpg", null=True, blank=True, upload_to='course_banner_pics')

    def __str__(self):
        return f"{self.course_name}"
  
    
class Content(models.Model):
    content_name = models.CharField(max_length=120)
    content = models.FileField(upload_to='uploaded_content')
    about = models.TextField(max_length=120)
    course_name = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='course_content')
    thumbnail = models.ImageField(default="default.jpg", null=True, blank=True, upload_to='content_thumbnail')
    date = models.DateField(auto_now=True)
    # duration = models.CharField(max_length=120)

    # existingPath = models.CharField(unique=True, max_length=100)
    # eof = models.BooleanField()

    def __str__(self):
        return f"course - {self.course_name} -- {self.content_name}"
        
    
   
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.PNG',null=True, blank=True, upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
   

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        # img = Image.open(self.image.name)
        img = Image.open(storage.open(self.image.path))
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.name)


@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Feedback(models.Model):
    comment = models.CharField(max_length=500)
    contentCommented = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.comment}"
  