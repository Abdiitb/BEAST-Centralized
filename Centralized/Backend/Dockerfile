# Use an official Python image
FROM python:3.12

# Environment variables to avoid creating .pyc files and enable real-time output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /backend

# Install system dependencies needed for building Python packages (like psycopg2)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev

# Install Poetry (for managing dependencies)
RUN pip install poetry

# Copy the poetry.lock and pyproject.toml (for dependency management)
COPY pyproject.toml poetry.lock ./

# Prevent poetry from creating a virtual environment, as we are using the global
# Python environment provided by the Docker image
RUN poetry config virtualenvs.create false

# Install dependencies using poetry
RUN poetry install --without dev

# Copy the rest of the application code
COPY . .

# Expose the port for the backend
EXPOSE 8000

# Set environment variable to determine if running in dev or prod
ENV ENV_MODE=prod

# For development, run Django development server with migrations
CMD ["sh", "-c", "if [ \"$ENV_MODE\" = \"dev\" ]; then echo \"Running in DEV mode\" && python manage.py makemigrations Authentication && python manage.py migrate && python manage.py runserver 0.0.0.0:8000; else echo \"Running in PROD mode\" && python manage.py collectstatic --noinput && gunicorn Backend.wsgi:application --bind 0.0.0.0:8000 --workers 3; fi"]