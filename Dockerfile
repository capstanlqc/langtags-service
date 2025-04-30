# use an official Python image as a base
FROM python:3.12

# install required system packages
RUN apt-get update && apt install -y wget gnupg && \
    wget -O- https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor | tee /usr/share/keyrings/adoptium-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/adoptium-keyring.gpg] https://packages.adoptium.net/artifactory/deb $(grep '^VERSION_CODENAME=' /etc/os-release | cut -d= -f2) main" | tee /etc/apt/sources.list.d/adoptium.list && \
    apt update && apt install -y temurin-21-jdk ant git && \
    rm -rf /var/lib/apt/lists/*

# set environment variables for Java 21 (only for the purpose of building openxliff)
# ENV JAVA_HOME="/home/souto/.sdkman/candidates/java/21.0.4-tem"
ENV JAVA_HOME="/usr/lib/jvm/temurin-21-jdk-amd64"
ENV PATH="$JAVA_HOME/bin:$PATH"

# create and set the working directory
WORKDIR /app

# install OpenXLIFF
RUN git clone https://github.com/rmraya/OpenXLIFF.git /app/opt/OpenXLIFF && \
    ant -f /app/opt/OpenXLIFF/build.xml
    # cd /app/opt/OpenXLIFF && ant

# install omegat
RUN mkdir -p /app/opt/omegat && wget https://cat.capstan.be/OmegaT/exe/5.7.3/OmegaT_5.7.3_Linux_64.tar.bz2 -P /app/opt && tar -xvjf /app/opt/OmegaT_5.7.3_Linux_64.tar.bz2 -C /app/opt/omegat && rm /app/opt/OmegaT_5.7.3_Linux_64.tar.bz2

# copy the project files
COPY . /app

# install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose the application port
EXPOSE 8000

# command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# uvicorn main:app --host 0.0.0.0 --port $PORT
