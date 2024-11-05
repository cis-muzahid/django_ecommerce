# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file into the image
COPY requirement.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirement.txt

COPY entrypoint.sh /app/

# Set environment variables for the Django application
ENV POSTGRES_DB=ecom
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432

ENTRYPOINT ["./entrypoint.sh"]
# Copy the rest of the application code into the image
COPY . /app/

# Expose port 8000 for the application
EXPOSE 8000
EXPOSE 5432

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
