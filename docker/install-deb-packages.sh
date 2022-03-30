#!/usr/bin/env bash

if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi


apt-get update


# general needed packages
apt-get install -y dirmngr
apt-get install -y apt-transport-https
apt-get install -y ca-certificates
apt-get install -y nodejs


# add R repository
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'

# needed R packages
apt-get install -y r-base
apt-get install -y build-essential
apt-get install -y pandoc
apt-get install -y xml2
apt-get install -y libssl-dev
apt-get install -y libxml2-dev
apt-get install -y libcurl4-openssl-dev
apt-get install -y libgit2-dev
apt-get install -y libfontconfig1-dev
