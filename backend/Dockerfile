# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container at /app
COPY requirements.txt /app/

# Install any dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port 8080 (or whatever port your Django app runs on)
EXPOSE 8080

# Run database migrations and then start the server
CMD ["sh", "-c", "python migrate.py && python manage.py runserver 0.0.0.0:8080"]
