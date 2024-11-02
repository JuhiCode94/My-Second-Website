from django import forms
from .models import CoverPicture, ProfilePicture, TimelinePicture

# Form for uploading a cover picture
class CoverPictureForm(forms.ModelForm):
    class Meta:
        model = CoverPicture
        fields = ['cover_picture'] # Include only the cover_picture field

# Form for uploading a profile picture
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ProfilePicture
        fields = ['profile_picture'] # Include only the profile_picture field

# Form for uploading a timeline picture
class TimelinePictureForm(forms.ModelForm):
    class Meta:
        model = TimelinePicture
        fields = ['timeline_picture'] # Include only the timeline_picture field
