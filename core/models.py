from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     email_token = models.CharField(max_length=200)
     forget_password_token = models.CharField(max_length=200 , null=True)
     is_verified = models.BooleanField(default=False)
     
     def __str__(self):
          return self.user.username
     
class Movie(models.Model):
     GENERE_CHOICES = [
          ('action', 'Action'),
          ('comedy','Comedy'),
          ('drama','Drama'),
          ('horror','Horror'),
          ('romance','Romance'),
          ('science_fiction','Science Fiction'),
          ('fantasy','Fantasy'),
     ]
     
     uu_id = models.UUIDField(default=uuid.uuid4)
     title = models.CharField(max_length=255)
     description = models.TextField()
     release_date = models.DateField()
     genere = models.CharField(max_length=255, choices=GENERE_CHOICES)
     length = models.PositiveIntegerField()
     image_card = models.ImageField(upload_to='movie_images/')
     image_cover = models.ImageField(upload_to='movie_images/')
     video = models.FileField(upload_to='movie_videos/')
     movie_views = models.IntegerField(default=0)
     
     def __str__(self):
          return self.title
     
class MovieList(models.Model):
     owner_user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, default=None)
     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
     