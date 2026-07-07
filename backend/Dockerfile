# Use official Python image as base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . .

# Expose the port Gunicorn will run on
EXPOSE 8000

# Run migrations and start Gunicorn server
CMD ["bash", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 ecom.wsgi:application"]

