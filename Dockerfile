# Use an official Python runtime as a base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install any needed system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
#pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY manage.py /app/manage.py
COPY templates /app/templates
COPY staticfiles /app/staticfiles
COPY tests /app/tests
COPY HairSaloon /app/HairSaloon
COPY nginx /app/nginx
COPY caller.py /app/caller.py

# Collect static files
RUN
