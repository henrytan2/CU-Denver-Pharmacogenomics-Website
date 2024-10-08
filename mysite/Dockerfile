# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies required for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements.txt file first (for caching dependencies)
COPY /mysite/requirements.txt /app

# Step 4: Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application code
COPY /mysite /app

# Step 6: Set environment variables (optional but good for security)
# You should set DJANGO_SECRET_KEY and other environment variables in docker-compose or a separate env file
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Step 7: Expose the port the app will run on
EXPOSE 8000

# Step 8: Run migrations and start the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# CMD ["/bin/bash"]
