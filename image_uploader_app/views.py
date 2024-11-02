from django.shortcuts import render, redirect, get_object_or_404
from .models import ImageUploaderUser, CoverPicture, ProfilePicture, TimelinePicture
from .forms import CoverPictureForm, ProfilePictureForm, TimelinePictureForm
from django.http import HttpResponse
import os
from django.contrib.auth.hashers import make_password, check_password  # Import for hashing
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone

# Create your views here.

# Welcome page view (Login page)
def welcome(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Attempt to log the user in by verifying the credentials
        try:
            user = ImageUploaderUser.objects.get(username=username)
            if check_password(password, user.password):  # Check the password
                # Update last_login field manually
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])

                login(request, user)  # Log the user in

                # Store logged-in username in session
                request.session['logged_in_username'] = user.username

                # Redirect to the user's home page with their username
                return redirect('home', username=user.username)
            else:
                messages.error(request, 'Invalid username or password')
        except ImageUploaderUser.DoesNotExist:
            messages.error(request, 'Invalid username or password')

    return render(request, 'welcome.html')

# Account creation view
def create_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # Check if username and password are at least 4 characters long
        if len(username) < 4 or len(password) < 4:
            messages.error(request, "Username and password must be at least 4 characters long.")
            return redirect('create_account')

        # Check if passwords match
        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('create_account')

        # Check if the username already exists
        if ImageUploaderUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('create_account')

        # Create a new user with hashed password
        user = ImageUploaderUser(username=username, password=make_password(password))
        user.save()
        messages.success(request, "Account created successfully!")
        
        # Log the user in and redirect to home
        login(request, user)
        request.session['logged_in_username'] = user.username  # Store username in session
        return redirect('home', username=user.username)  # Redirect to home page

    return render(request, 'create_account.html')

# Password reset view
def forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        # Check if the username exists in the database
        try:
            user = ImageUploaderUser.objects.get(username=username)
        except ImageUploaderUser.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('forgot_password')

        # Check if the new password and confirm password are the same
        if new_password != confirm_new_password:
            messages.error(request, 'Passwords do not match')
            return redirect('forgot_password')

        # Check if the password is at least 4 characters long
        if len(new_password) < 4:
            messages.error(request, 'Password must be at least 4 characters long')
            return redirect('forgot_password')

        # Everything is correct, set the new password
        user.password = make_password(new_password)  # This hashes the password
        user.save()

        messages.success(request, 'Password reset successfully')
        
        # Log the user in and redirect to home
        login(request, user)
        request.session['logged_in_username'] = user.username  # Store username in session
        return redirect('home', username=user.username)  # Redirect to home page

    return render(request, 'forgot_password.html')

# Home page view with forms to upload pictures
def home(request, username):
    user = ImageUploaderUser.objects.get(username=username)

    if request.method == 'POST':
        # Handle cover picture upload
        if 'cover_picture' in request.FILES:
            cover_photo_form = CoverPictureForm(request.POST, request.FILES)
            if cover_photo_form.is_valid():
                cover_picture = cover_photo_form.save(commit=False)
                cover_picture.user = user  # Set the user to the current user
                cover_picture.save()  # Save the cover picture
                return redirect('home', username=user.username)
        # Handle profile picture upload    
        elif 'profile_picture' in request.FILES:
            profile_photo_form = ProfilePictureForm(request.POST, request.FILES)
            if profile_photo_form.is_valid():
                profile_picture = profile_photo_form.save(commit=False)
                profile_picture.user = user  # Set the user to the current user
                profile_picture.save()  # Save the profile picture
                return redirect('home', username=user.username)
        # Handle timeline picture upload    
        elif 'timeline_picture' in request.FILES:
            timeline_photo_form = TimelinePictureForm(request.POST, request.FILES)
            if timeline_photo_form.is_valid():
                timeline_picture = timeline_photo_form.save(commit=False)
                timeline_picture.user = user  # Set the user to the current user
                timeline_picture.save()  # Save the timeline picture
                return redirect('home', username=user.username)

    # Initialize blank forms if no files were uploaded
    cover_photo_form = CoverPictureForm()
    profile_photo_form = ProfilePictureForm()
    timeline_photo_form = TimelinePictureForm()

    context = {
        'user': user,
        'latest_cover_photo': user.cover_pictures.last(),
        'latest_profile_photo': user.profile_pictures.last(),
        'all_timeline_photos': user.timeline_pictures.all(),
        'cover_photo_form': cover_photo_form,
        'profile_photo_form': profile_photo_form,
        'timeline_photo_form': timeline_photo_form,
    }
    return render(request, 'home.html', context)

# View for displaying the Photos page for a specific user
def photos(request, username):
    # Get the user object by username or return a 404 error if not found
    user = get_object_or_404(ImageUploaderUser, username=username)
    
    # Query the cover, profile, and timeline photos related to the user
    cover_photos = CoverPicture.objects.filter(user=user)
    profile_photos = ProfilePicture.objects.filter(user=user)
    timeline_photos = TimelinePicture.objects.filter(user=user)

    # Pass the queried photos to the template
    context = {
        'user': user,
        'cover_photos': cover_photos,
        'profile_photos': profile_photos,
        'timeline_photos': timeline_photos
    }
    # Render the photos page with the context
    return render(request, 'photos.html', context)

# View for deleting a specific photo based on its type (cover, profile, or timeline)
def delete_photo(request, username, photo_type, photo_id):
    # Get the user object by username or return a 404 error if not found
    user = get_object_or_404(ImageUploaderUser, username=username)

    # Retrieve the appropriate photo object based on the photo_type and photo_id
    if photo_type == 'cover':
        photo = get_object_or_404(CoverPicture, id=photo_id, user=user)
        image_field = photo.cover_picture  # Access the correct image field
    elif photo_type == 'profile':
        photo = get_object_or_404(ProfilePicture, id=photo_id, user=user)
        image_field = photo.profile_picture  # Access the correct image field
    elif photo_type == 'timeline':
        photo = get_object_or_404(TimelinePicture, id=photo_id, user=user)
        image_field = photo.timeline_picture  # Access the correct image field

    # Check if the request method is POST (i.e., deletion request)
    if request.method == 'POST':
        # Delete the image file from the filesystem if it exists
        if image_field and os.path.isfile(image_field.path):
            os.remove(image_field.path)

        # Delete the photo entry from the database
        photo.delete()

        # Redirect back to the photos page after deletion
        return redirect('photos', username=user.username)

    # Return a 405 status code if the request method is not allowed
    return HttpResponse(status=405)

# View for displaying a user's profile details
def profile_details(request, username):
    # Get the user object by username or return a 404 error if not found
    user = get_object_or_404(ImageUploaderUser, username=username)
    
    # Pass the user object to the profile details template
    context = {
        'user': user,
    }

    # Render the profile details page
    return render(request, 'profile_details.html', context)

# View for logging out the user
def logout_view(request):
    # Log out the current user
    logout(request)

    # Redirect to the welcome page after logout
    return redirect('welcome') 

# View for searching users by their username
def search_user(request):
    # Get the search query (username) from the GET request
    search_query = request.GET.get('username')

    # If no username is provided, show an error message
    if not search_query:
        messages.error(request, "Please enter a username to search.")
        # Redirect back to the referring page, retaining the logged-in user's session
        return redirect(request.META.get('HTTP_REFERER', 'home'), username=request.session['logged_in_username'])

    try:
        # Try to find a user by the searched username
        searched_user = ImageUploaderUser.objects.get(username=search_query)
        # Redirect to the searched user's profile if found
        return redirect('view_user_profile', username=searched_user.username)
    
    except ImageUploaderUser.DoesNotExist:
        # If the user does not exist, display an error message
        messages.error(request, 'User not found.')
        # Redirect back to the referring page, retaining the logged-in user's session
        return redirect(request.META.get('HTTP_REFERER', 'home'), username=request.session['logged_in_username'])

# View for displaying a specific user's profile and their latest photos
def view_user_profile(request, username):
    # Get the user object by username or return a 404 error if not found
    user = get_object_or_404(ImageUploaderUser, username=username)

    # Prepare the context with the latest cover photo, profile photo, and all timeline photos
    context = {
        'user': user,
        'latest_cover_photo': user.cover_pictures.last(), # Get the latest cover picture
        'latest_profile_photo': user.profile_pictures.last(), # Get the latest profile picture
        'all_timeline_photos': user.timeline_pictures.all(), # Get all timeline photos
    }

    # Render the user's profile page with their photos
    return render(request, 'view_user_profile.html', context)  

# View for displaying a user's latest photos (cover, profile, timeline) on a dedicated page
def view_user_photos(request, username):
    # Get the user object by username or return a 404 error if not found
    user = get_object_or_404(ImageUploaderUser, username=username)
    
    # Retrieve all cover, profile, and timeline photos for the user
    cover_photos = user.cover_pictures.all()  # Get all cover pictures
    profile_photos = user.profile_pictures.all()  # Get all profile pictures
    all_timeline_photos = TimelinePicture.objects.filter(user=user) # Retrieve all timeline photos

    # Pass the photos and user information to the template
    context = {
        'user': user,
        'cover_photos': cover_photos,
        'profile_photos': profile_photos,
        'all_timeline_photos': all_timeline_photos,
    }

    # Render the user's photos page
    return render(request, 'view_user_photos.html', context)