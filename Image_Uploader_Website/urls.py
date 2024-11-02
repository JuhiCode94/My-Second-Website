"""
URL configuration for Image_Uploader_Website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from image_uploader_app import views # Import views from the image uploader app

# Define the list of URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls), # Admin page for site administrators
    
    # Home and authentication-related URLs
    path('', views.welcome, name='welcome'), # Landing or welcome page
    path('login/', views.welcome, name='login'), # Login page (mapped to welcome for now)
    path('logout/', views.logout_view, name='logout'), # Logout view to log out users
    path('create-account/', views.create_account, name='create_account'), # Account creation page
    path('forgot-password/', views.forgot_password, name='forgot_password'), # Password reset page

    # User-related URLs
    path('home/<str:username>/', views.home, name='home'),  # Home page for the specific user

    # URL to view and manage photos of a specific user
    path('<str:username>/photos/', views.photos, name='photos'), # View user's photos
    path('<str:username>/delete_photo/<str:photo_type>/<int:photo_id>/', views.delete_photo, name='delete_photo'),  # Delete a specific user photo

    # URL for viewing and editing user profile details
    path('<str:username>/profile_details/', views.profile_details, name='profile_details'), # User profile details

    # URL for user search functionality
    path('search/', views.search_user, name='search_user'), # Search for a user by username

    # URLs for viewing a specific user's profile and their photos
    path('user/<str:username>/', views.view_user_profile, name='view_user_profile'), # View another user's profile
    path('user/<str:username>/photos/', views.view_user_photos, name='view_user_photos'), # View another user's photos
] 

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
