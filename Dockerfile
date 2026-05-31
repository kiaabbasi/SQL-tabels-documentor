# Use an official Python runtime as a parent image
# FROM python:3.9-slim

FROM dockerhub.um.ac.ir/devops/python:3.12-slim

RUN rm -rf /etc/apt/sources.list.d/*

RUN echo "deb [trusted=yes] http://repos.um.ac.ir/debian bookworm main contrib non-free-firmware \
deb [trusted=yes] http://repos.um.ac.ir/debian bookworm-updates main contrib non-free-firmware \
deb [trusted=yes] http://repos.um.ac.ir/debian bookworm-backports main contrib non-free-firmware \
deb [trusted=yes] http://repos.um.ac.ir/debian-security bookworm-security main contrib non-free-firmware " \
    > /etc/apt/sources.list && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install telnet gcc python3-dev default-libmysqlclient-dev build-essential pkg-config -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Set the working directory
WORKDIR /app

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

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
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
