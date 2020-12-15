

    cd tools/framework
    make installrequirementsR
    sudo R

start R CLI with: `R` and execute:

    install.packages("rmarkdown")
    install.packages("rmdformats")
    install.packages("kableExtra")
    install.packages("openssl")
    install.packages("withr")
    # maybe a restart is required

    quit()
    n   # save workspace

sometimes a additional manual execution within `R Studio Desktop` of `meshReport.Rmd` may also help
