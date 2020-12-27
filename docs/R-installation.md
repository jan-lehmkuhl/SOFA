
R CLI
================================================================================

    cd tools/framework
    make installrequirementsR
    sudo R

start R CLI with: `R` and execute:

    install.packages("rmarkdown")
    install.packages("rmdformats")
    install.packages("kableExtra")
    install.packages("openssl")
    install.packages("withr")
    install.packages("shiny")
    install.packages("ggplot2")
    # maybe a restart is required

    quit()
    n   # save workspace



R Studio Desktop
================================================================================

sometimes a additional manual execution within `R Studio Desktop` of `meshReport.Rmd` may also help:  
https://rstudio.com/products/rstudio/download/#download

    cd STUDY/mesh/MESHCASE
    cd doc/meshReport
    rstudio meshReport.Rmd
