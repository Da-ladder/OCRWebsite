# Dockerfile
# FOR WINDOWS ONLY

# Use Python Alpine Linux base image
FROM python:3.11.4-alpine

# Set working directory
WORKDIR /usr/src/app

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure Python output is sent directly to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Copy requirements.txt and install Python dependencies
COPY ./helloWorld/testBranch/requirements.txt /usr/src/app/requirements.txt
RUN python3 -m pip install -r requirements.txt

# Copy entrypoint script
COPY ./helloWorld/testBranch/entrypoint.sh /usr/src/app/entrypoint.sh

# Copy application code
COPY . /usr/src/app/

# Set entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
