# Use the official Python image from the Docker Hub
FROM python:3.11.4-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN adduser --disabled-password appuser

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project files into the container
COPY . .

# Run collectstatic to gather all static files
RUN python manage.py collectstatic --noinput

# Create static files directory
RUN mkdir -p /app/staticfiles && \
    chown -R appuser:appuser /app/staticfiles

# Change to the non-root user
USER appuser

# Command to run the application (change this according to your entry point)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Image_Uploader_Website.wsgi:application"]