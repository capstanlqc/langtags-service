#!/bin/bash
mkdir -p /opt/glibc-2.38
cd /opt/glibc-2.38
curl -LO http://ftp.gnu.org/gnu/libc/glibc-2.38.tar.gz
tar -xzf glibc-2.38.tar.gz
cd glibc-2.38
mkdir build
cd build
../configure --prefix=/opt/glibc-2.38
make -j$(nproc)
make install
export LD_LIBRARY_PATH=/opt/glibc-2.38/lib:$LD_LIBRARY_PATH

apt-get update
# apt-get update && apt-get install -y libc6=2.38-1
apt-get install -y openjdk-21-jdk ant