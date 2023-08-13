#!/bin/bash
HEADLESS=1

# General Updates
sudo apt-get update
sudo apt-get upgrade
sudo apt-get autoremove -y

# LXStudio Installation instructions
# https://github.com/heronarts/LXStudio/wiki/Getting-Started

# Install temurin-17-jdk
# From here: https://adoptium.net/installation/linux/
#https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8%2B7/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.8_7.tar.gz
sudo apt install -y wget apt-transport-https
sudo mkdir -p /etc/apt/keyrings
wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | sudo tee /etc/apt/keyrings/adoptium.asc
echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | sudo tee /etc/apt/sources.list.d/adoptium.list
sudo apt update # update if you haven't already
sudo apt install temurin-17-jdk -y

# Install Eclipse
# List of mirrors here: https://www.eclipse.org/downloads/download.php?file=/oomph/epp/2023-06/R/eclipse-inst-jre-linux-aarch64.tar.gz
if [[ $HEADLESS -eq 0 ]]
  mkdir ~/eclipse-workspace
  wget "https://mirrors.jevincanders.net/eclipse/oomph/epp/2023-06/R/eclipse-inst-jre-linux-aarch64.tar.gz" -O ./eclipse-workspace/eclipse-inst-jre-linux-aarch64.tar.gz
  tar xvzf ./eclipse-workspace/eclipse-inst-jre-linux-aarch64.tar.gz
  ~/eclipse-installer/eclipse-inst
fi

# Clone repositories
# Pleasure Dairy
sudo apt-get install git -y
mkdir ~/git
# Pleasure Dairy
git -C ~/git clone git@github.com:jcm-art/pleasure-dairy.git
git -C ~/git/pleasure-dairy/ submodule update --init --recursive
# LX Studio
git -C ~/git clone git@github.com:heronarts/LXStudio-IDE.git


