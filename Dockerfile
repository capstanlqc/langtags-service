# Use an official Python image as a base
FROM python:3.12

# Install required system packages
RUN apt-get update && apt install -y wget gnupg && \
    wget -O- https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor | tee /usr/share/keyrings/adoptium-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/adoptium-keyring.gpg] https://packages.adoptium.net/artifactory/deb $(grep '^VERSION_CODENAME=' /etc/os-release | cut -d= -f2) main" | tee /etc/apt/sources.list.d/adoptium.list && \
    apt update && apt install -y temurin-21-jdk ant git && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for Java
# ENV JAVA_HOME="/home/souto/.sdkman/candidates/java/21.0.4-tem"
ENV JAVA_HOME="/usr/lib/jvm/temurin-21-jdk-amd64"
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
# uvicorn main:app --host 0.0.0.0 --port $PORT