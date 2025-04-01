# Use an official Python image as a base
FROM python:3.12

# Install required system packages
RUN apt-get update && \
    apt-get install -y openjdk-21-jdk ant && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for Java
ENV JAVA_HOME="/usr/lib/jvm/java-21-openjdk-amd64"
ENV PATH="$JAVA_HOME/bin:$PATH"

# Create and set the working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]