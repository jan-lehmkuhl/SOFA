
R CLI
================================================================================

    cd tools/framework
    make installrequirementsR
    sudo Rscript -e 'install.packages("rmarkdown")'
    sudo Rscript -e 'install.packages("rmdformats")'
    sudo Rscript -e 'install.packages("kableExtra")'
    sudo Rscript -e 'install.packages("openssl")'
    sudo Rscript -e 'install.packages("withr")'
    sudo Rscript -e 'install.packages("shiny")'
    sudo Rscript -e 'install.packages("ggplot2")'
    # maybe a restart is required



R Studio Desktop
================================================================================

sometimes a additional manual execution within `R Studio Desktop` of `meshReport.Rmd` may also help:  
https://rstudio.com/products/rstudio/download/#download

    cd STUDY/mesh/MESHCASE
    cd doc/meshReport
    rstudio meshReport.Rmd
