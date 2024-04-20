# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
# Copy the requirements file first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
#COPY . /app
COPY manage.py /app/manage.py
COPY static_collected /app/static_collected
COPY staticfiles /app/staticfiles
COPY templates /app/templates
COPY tests /app/tests
COPY nginx /app/nginx
COPY HairSaloon /app/HairSaloon
