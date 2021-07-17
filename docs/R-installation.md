
R CLI
================================================================================

    cd tools/framework
    make installrequirementsR
    sudo R 

beside the normal package installation which is done by `install.packages("PACKAGE")` one particular have to be added manual: 
~~~
devtools::install_git("https://gitlab.com/sofa-framework/ofreportr-core")
~~~

## troubleshooting
* maybe a restart is required
* often also an execution of the `*.Rmd` file with the `rstudio` GUI helps with installation issues 



R Studio Desktop
================================================================================

sometimes a additional manual execution within `R Studio Desktop` of `meshReport.Rmd` may also help:  
https://rstudio.com/products/rstudio/download/#download

    cd STUDY/mesh/MESHCASE
    cd doc/meshReport
    rstudio meshReport.Rmd
