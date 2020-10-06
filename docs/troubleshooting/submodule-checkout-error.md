
# submodule update
If you forgot to clone `--recursive` then submodules can be load with: 

    git submodule update --init


# wrong branch
sometimes the project repo dont refer to the `master` in the submodules. Then you get some errors like this: 
[IdeaLink](https://youtrack.jetbrains.com/issue/TW-63901) 

    Submodule 'tools/framework' (git@gitlab.com:sofa-framework/core.git) registered for path 'tools/framework'
    Submodule 'tools/openFoam-reporting' (git@gitlab.com:HS-GM_OpenFOAM/r_openfoam) registered for path 'tools/openFoam-reporting'
    Submodule 'tools/openFoam-setup' (git@gitlab.com:HS-GM_OpenFOAM/openFoamSetup.git) registered for path 'tools/openFoam-setup'
    Cloning into 'C:/Users/lehmk/isac/schadstoffe/tools/framework'...
    Cloning into 'C:/Users/lehmk/isac/schadstoffe/tools/openFoam-reporting'...
    Cloning into 'C:/Users/lehmk/isac/schadstoffe/tools/openFoam-setup'...
    fatal: git upload-pack: not our ref 9f4d5941ee2d64e3bc0f10124d23b030420989d5fatal: remote error: upload-pack: not our ref 9f4d5941ee2d64e3bc0f10124d23b030420989d5
    Fetched in submodule path 'tools/framework', but it did not contain 9f4d5941ee2d64e3bc0f10124d23b030420989d5. Direct fetching of that commit failed.

The important part is `not our ref`.  To fix this you have to checkout the branch with the referenced commit
