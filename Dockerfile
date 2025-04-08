# Use the official Python slim image (small & efficient)
FROM python:3.12.6-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=WonderSri_backend.settings

# Install GDAL, GEOS, and required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    python3-gdal \
    && rm -rf /var/lib/apt/lists/*

# Verify GDAL installation
RUN gdalinfo --version

# Set the working directory
WORKDIR /app

# Copy requirements file first (to use Docker caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Expose port 10000 (required by Render)
EXPOSE 10000

# Run migrations and start the Django application with Daphne
CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 10000 --proxy-headers WonderSri_backend.asgi:application"]
