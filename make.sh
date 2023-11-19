#!/bin/bash
havecmd() {
    type "$1" &> /dev/null
}
CWD=$(echo $(command cd $(dirname '$0'); pwd))

## GLOBAL VARIABLES
## -----------------------------------------------------------------------------
PGWD=$CWD/postgres
CONDAENV=tweetcaption

if [[ $(basename "${0}") != "make.sh" ]]; then
    # Script sourced, load or create condaenv
    if conda info --envs | grep -q $CONDAENV; then
        conda activate $CONDAENV
    else
        echo "Setting up $CONDAENV conda environment."
        conda create -n $CONDAENV python=3.10 -c conda-forge
        conda activate $CONDAENV
    fi
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
    conda install -c conda-forge cxx-compiler==1.5.2 # gcc11
    conda install -c conda-forge cudatoolkit cudatoolkit-dev
    conda install -c conda-forge postgresql=16

    pip -v install -r $CWD/requirements.txt
    # npm install
}

update() {
    pip -v install -r $CWD/requirements.txt
    python $CWD/server/conf.py
}

build() {
    ## Compile all items and build the docker container.
    npm run build
}

run() {
    cd $BWD
    export WS_USE_PG=0

    if [[ -n $WS_USE_PG && -z $WS_DB_PSWD ]]; then
        echo "Plase export WS_DB_PSWD with pgdev install password."
        exit 20
    fi

    python manage.py runserver
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

config() {
    # Create/Update yaml config file.
    python $CWD/backend/conf.py    
}


## EXECUTE OR SHOW USAGE.
## -----------------------------------------------------------------------------
if [[ "$#" -lt 1 ]]; then
    echo -e "USAGE: $0 <command> [options...]\n"
    echo -e "Available commands:\n"

    echo -e "build              - Run build on server backend and frontend."
    echo -e "run                - Run the server locally."

    echo -e "postgres           - Run the postgres docker container."
    echo -e "pgshell            - Login to the running postgres server."

    echo -e "install            - Run conda and npm installation."
    echo -e "config             - Create or update config file."
    echo -e "update             - Run update."
    echo -e "install_nodejs     - Install nvm, node, npm in HOME."
    echo -e "update_nodejs      - Update node and npm using nvm."
    echo

else
    "$@"
    cd $CWD
fi
