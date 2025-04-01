#!/bin/bash
apt update && apt install -y wget gnupg  
wget -O- https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor | tee /usr/share/keyrings/adoptium-keyring.gpg > /dev/null  
echo "deb [signed-by=/usr/share/keyrings/adoptium-keyring.gpg] https://packages.adoptium.net/artifactory/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/adoptium.list  
apt update && apt install -y temurin-21-jdk  

apt-get install -y ant