#!/usr/bin/env bash

if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi


# this packages can also be installed within `sudo R` shell

Rscript -e 'install.packages("rmarkdown")'
Rscript -e 'install.packages("rmdformats")'
Rscript -e 'install.packages("kableExtra")'
Rscript -e 'install.packages("openssl")'
Rscript -e 'install.packages("withr")'
Rscript -e 'install.packages("shiny")'
Rscript -e 'install.packages("ggplot2")'
Rscript -e 'install.packages("devtools")'
Rscript -e 'install.packages("fastmap")'
Rscript -e 'install.packages("rjson")'
