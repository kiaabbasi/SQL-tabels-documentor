# Use an official Python runtime as a parent image
# FROM python:3.9-slim

FROM dockerhub.um.ac.ir/devops/fastapi-skeleton-web:py3.12.5

#RUN apt-get update && apt-get install -y \
#    gcc \
#    default-libmysqlclient-dev \
#    build-essential \
#    pkg-config \
#    && rm -rf /var/lib/apt/lists/*



# Set the working directory
WORKDIR /app

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app/app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt --index-url https://dockerhub.um.ac.ir/repository/pypi-proxy/simple

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
