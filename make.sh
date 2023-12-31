#!/bin/bash
havecmd() {
    type "$1" &> /dev/null
}
CWD=$(echo $(command cd $(dirname '$0'); pwd))

## GLOBAL VARIABLES
## -----------------------------------------------------------------------------
PGWD=$CWD/postgres
CONDAENV=pyworkman

if [[ $(basename "${0}") != "make.sh" ]]; then
    # Script sourced, load or create condaenv
    if conda info --envs | grep -q $CONDAENV; then
        conda activate $CONDAENV
        export PYTHONPATH=.
    else
        echo "Setting up $CONDAENV conda environment."
        conda create -n $CONDAENV python=3.10 -c conda-forge
        conda activate $CONDAENV
    fi

    alias make="$CWD/make.sh"
    echo "Environment set up. You can now use 'make' to execute this script."
    return 0
fi

install_nodejs() {
    # Install nvm
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash

    # Load nvm
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

    # Install node
    nvm install node
}

update_nodejs() {
    # Load nvm
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

    # Update node
    nvm install node
    nvm alias default node
}

install() {
    pip -v install -e .
    cd $CWD/workman/ui
    npm install
}

build() {
    ## Compile all items necessary.
    cd $CWD/workman/ui
    npm run build
}

postgres() {
    # PG database for development.
    # Use the host network for other containers.

    cd $PGWD
    docker build -t pgserv .

    # Run this to fix the permissions of a persistent volume.
    # sudo chown 1024:1024 ./pgserv_data

    # Remove previous if any.
    docker stop pgserv && docker container rm pgserv

    # Run in background using volume for persistence.
    docker run -itd -v $CWD/postgres/pg_data/:/data/ --net=host \
        --name pgserv pgserv

    # Check running.
    echo
    docker ps

    # Help message.
    echo -e "Login to the container using:"
    echo -e "\tdocker exec -it pgserv bash"
    echo -e "If database is not setup, run 'install', 'create' first."
    echo -e "Rerun the container to start the server.\n"

    # Follow logs.
    docker logs -f pgserv
}

pgshell() {
    docker exec -it pgserv bash
}

bump() {
    ## Bump the version number
    grep version pyproject.toml
    VERSION=$(sed -n 's/version = "\(.*\)"/\1/p' pyproject.toml)
    VERSION=$(python -c "v='$VERSION'.split('.');print('%s.%s.%d' %(v[0], v[1], int(v[2])+1))")
    echo "   >>>"
    sed -i "s/\(version = \"\)[^\"]*\"/\1$VERSION\"/" pyproject.toml
    sed -i "s/\(__version__ = \"\)[^\"]*\"/\1$VERSION\"/" workman/__init__.py
    grep version pyproject.toml
    git add pyproject.toml workman/__init__.py
}

tag() {
    # create a new git tag using the pyproject.toml version
    # and push the tag to origin
    version=$(sed -n 's/version = "\(.*\)"/\1/p' pyproject.toml)
    git tag v$version && git push origin v$version
}


## EXECUTE OR SHOW USAGE.
## -----------------------------------------------------------------------------
if [[ "$#" -lt 1 ]]; then
    echo -e "USAGE: $0 <command> [options...]\n"
    echo -e "Available commands:\n"

    echo -e "build              - Run build on server backend and frontend."
    echo -e "bump               - Bump the package minor version number."
    echo -e "tag                - Tag current version and push to origin."

    echo -e "postgres           - Run the postgres docker container."
    echo -e "pgshell            - Login to the running postgres server."

    echo -e "install            - Run conda and npm installation."
    echo -e "install_nodejs     - Install nvm, node, npm in HOME."
    echo -e "update_nodejs      - Update node and npm using nvm."
    echo

else
    "$@"
    cd $CWD
fi
