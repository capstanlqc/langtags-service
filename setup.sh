#!/bin/bash
nix profile install nixpkgs#glibc
export LD_LIBRARY_PATH=$HOME/.nix-profile/lib:$LD_LIBRARY_PATH
apt-get update
# apt-get update && apt-get install -y libc6=2.38-1
apt-get install -y openjdk-21-jdk ant