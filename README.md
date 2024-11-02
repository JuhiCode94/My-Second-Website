# Image Uploader Website

![Logo](static/img/favicon.ico)

This is a Django-based application for uploading and managing images. Users can upload cover pictures, profile pictures, and timeline images while enjoying a responsive and user-friendly interface. Additionally, users can view other users' uploaded photos, fostering a community experience.

## Table of Contents
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Docker](#docker)

## Features

- User authentication (registration and login).
- Upload and manage images (cover, profile, timeline).
- Responsive design for mobile and desktop views.
- Admin panel to manage uploaded images.

## Setup

**Create a virtual environment and activate it:**

    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

**Install the required packages:**

    ```
    pip install -r requirements.txt
    ```

**Apply migrations:**

    ```
    python manage.py migrate
    ```

### Technologies Used

- **Python**: 3.11.4
- **Django**: 5.0.6
- **Gunicorn**: For serving the application in production
- **Pillow**: For image handling
- **ASGIREF**: For asynchronous handling

**Run the development server:**

    ```sh
    python manage.py runserver
    ```

**Open your browser and navigate to:** `http://127.0.0.1:8000`

### Usage

#### URLs and Views

- **Welcome Page:** `http://127.0.0.1:8000/`
- **Forgot-Password Page:** `http://127.0.0.1:8000/forgot-password/`
- **Create-Account Page:** `http://127.0.0.1:8000/create-account/`
- **Homw Page:** `http://127.0.0.1:8000/home/`
- **Photos Page:** `http://127.0.0.1:8000/photos/`
- **Profile-Details Page:** `http://127.0.0.1:8000/profile_details/`
- **User Page:** `http://127.0.0.1:8000/user/`
- **User-Photos Page:** `http://127.0.0.1:8000/user/praveen/photos/`

#### Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin` with the following credentials:

- **Username:** admin
- **Password:** admin_password

### Project Structure

```plaintext
image_uploader/
├── image_uploader_app/
│   ├── migrations/
│   ├── static/
│   │   └── img/
│   ├── templates/
│   │   ├── upload.html
│   │   ├── gallery.html
│   │   └── profile.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── Image_Uploader_Website/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/
│   ├── cover_pictures/
│   ├── profile_pictures/
│   └── timeline_pictures/
├── manage.py
└── requirements.txt

```
## Docker

Docker support is available for this project. For detailed instructions on how to build and run the application using Docker, please refer to the [Docker-specific README](README.Docker.md).
