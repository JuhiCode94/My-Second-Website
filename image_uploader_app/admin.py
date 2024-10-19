from django.contrib import admin
from .models import ImageUploaderUser, CoverPicture, ProfilePicture, TimelinePicture

# Register your models here.

# Admin customization for ImageUploaderUser
class ImageUploaderUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_login') # Display username and last login in the admin list

# Register ImageUploaderUser model
admin.site.register(ImageUploaderUser, ImageUploaderUserAdmin)

# Admin customization for CoverPicture
class CoverPictureAdmin(admin.ModelAdmin):
    readonly_fields = ('uploaded_at',) # Make the uploaded_at field read-only
    list_display = ('user', 'cover_picture', 'uploaded_at') # Display user, picture, and upload time
    search_fields = ('user__username',) # Enable search by username

# Register CoverPicture model
admin.site.register(CoverPicture, CoverPictureAdmin)

# Admin customization for ProfilePicture
class ProfilePictureAdmin(admin.ModelAdmin):
    readonly_fields = ('uploaded_at',) # Make the uploaded_at field read-only
    list_display = ('user', 'profile_picture', 'uploaded_at') # Display user, picture, and upload time
    search_fields = ('user__username',) # Enable search by username

# Register ProfilePicture model
admin.site.register(ProfilePicture, ProfilePictureAdmin)

# Admin customization for TimelinePicture
class TimelinePictureAdmin(admin.ModelAdmin):
    readonly_fields = ('uploaded_at',) # Make the uploaded_at field read-only
    list_display = ('user', 'timeline_picture', 'uploaded_at') # Display user, picture, and upload time
    search_fields = ('user__username',)  # Enable search by username

# Register TimelinePicture model
admin.site.register(TimelinePicture, TimelinePictureAdmin)
