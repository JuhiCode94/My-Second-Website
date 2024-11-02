from django.db import models
from django.contrib.auth.hashers import check_password

# Create your models here.

# Define the custom user model for image uploader
class ImageUploaderUser(models.Model):
    username = models.CharField(max_length=150, unique=True) # Unique username field
    password = models.CharField(max_length=128) # Store hashed password
    last_login = models.DateTimeField(null=True, blank=True) # Track last login time

    def __str__(self):
        return self.username
    
    # Method to check if the given password matches the stored hashed password
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

# Model for storing user's cover pictures
class CoverPicture(models.Model):
    user = models.ForeignKey(ImageUploaderUser, on_delete=models.CASCADE, related_name='cover_pictures') # Link to user
    cover_picture = models.ImageField(upload_to='cover_pictures/') # Path to save cover picture
    uploaded_at = models.DateTimeField(auto_now_add=True) # Timestamp for when the picture was uploaded

# Model for storing user's profile pictures
class ProfilePicture(models.Model):
    user = models.ForeignKey(ImageUploaderUser, on_delete=models.CASCADE, related_name='profile_pictures') # Link to user
    profile_picture = models.ImageField(upload_to='profile_pictures/') # Path to save profile picture
    uploaded_at = models.DateTimeField(auto_now_add=True) # Timestamp for when the picture was uploaded

# Model for storing user's timeline pictures
class TimelinePicture(models.Model):
    user = models.ForeignKey(ImageUploaderUser, on_delete=models.CASCADE, related_name='timeline_pictures') # Link to user
    timeline_picture = models.ImageField(upload_to='timeline_pictures/') # Path to save timeline picture
    uploaded_at = models.DateTimeField(auto_now_add=True) # Timestamp for when the picture was uploaded    
