#!/usr/bin/env bash

if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi


apt-get update


# general needed packages
apt-get install -y nodejs


# needed R packages
apt-get install -y r-base
apt-get install -y pandoc
apt-get install -y xml2
apt-get install -y libssl-dev
apt-get install -y libxml2-dev
apt-get install -y libcurl4-openssl-dev
apt-get install -y libgit2-dev
apt-get install -y libfontconfig1-dev
