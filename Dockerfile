# Base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Copy entrypoint script and give execution permissions
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

# Make entrypoint script the container's entrypoint
ENTRYPOINT ["./docker-entrypoint.sh"]
# Run server (development mode)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
