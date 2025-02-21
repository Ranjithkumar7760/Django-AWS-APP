# Use official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Ensure Django settings are properly set before collectstatic
ENV DJANGO_SETTINGS_MODULE=healthcare.settings

# **Fix: Create Static Directory before Running collectstatic**
RUN mkdir -p /app/healthcare/static

# Run collectstatic after ensuring dependencies are installed
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "healthcare.wsgi:application"]
