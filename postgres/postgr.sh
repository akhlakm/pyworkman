#!/bin/bash

install() {
    # Create a new postgres server inside PGDATA directory.
    # Ask for the superuser password.
    initdb -U $POSTGRES_USER --pwprompt 
}

run() {
    # Check if the server is running or start it.

    # Fix permission issue.
    chmod 0750 $PGDATA

    if ! pg_ctl status; then
        # Overwrite the existing conf file.
        if [[ -f $PGDATA/PG_VERSION ]]; then
            mv -f /postgres/_postgresql.conf $PGDATA/postgresql.conf
            mv -f /postgres/_pg_hba.conf $PGDATA/pg_hba.conf
        fi
        pg_ctl -o "-F -p $POSTGRES_PORT" start 
    fi
}

shell() {
    # PSQL shell into a database.

    if [[ -n $1 ]]; then 
        psql -U $POSTGRES_USER -p $POSTGRES_PORT $1
    else
        echo "USAGE: shell <db name>"
        return 1
    fi
}

create() {
    # Create a new database.

    if [[ -n $1 ]]; then
        createdb -U $POSTGRES_USER -p $POSTGRES_PORT $1
    else
        echo "USAGE: create <db name>"
        return 1
    fi
}

stop() {
    # Stop Postgres server.
    pg_ctl -U $POSTGRES_USER -p $POSTGRES_PORT stop
}

backup-db() {
    # Make a backup of a specific database to a directory.

    if [[ -n $1 ]]; then
        echo "Running backup ..."
        bkdir=$MNTVOL/backup/$(date '+%b%d_%Y')/${1}
        mkdir -p $bkdir
        # Create backup with 4 processes, in directory format,
        # with default compression
        pg_dump -v -U $POSTGRES_USER -p $POSTGRES_PORT \
                -j 4 -F d -f $bkdir -d ${1}
        echo "Backup Done! Saved to $bkdir"
    else
        echo "USAGE: backup-db <db name>"
        return 1
    fi
}

backup-table() {
    # Make a backup of a specific table to a file.

    if [[ -n $1 ]] && [[ -n $2 ]]; then
        echo "Running backup ..."
        bkdir=$MNTVOL/backup/$(date '+%b%d_%Y')/
        cfile="$bkdir/${1}-${2}.pgdump"
        mkdir -p $bkdir
        # Create backup in custom compressed format.
        pg_dump -v -U $POSTGRES_USER -p $POSTGRES_PORT \
                -F c -f $cfile -d ${1} -t ${2}
        echo "Backup Done! Saved to $cfile"
    else
        echo "USAGE: backup-table <db name> <table name>"
        return 1
    fi
}

backup-info() {
    # Show information about a backup file/directory.

    if [[ -n $1 ]]; then
        pg_restore -l "$1"

        if [[ -d $1 ]]; then 
            echo "Restore dir to database: '$0 restore-db'"
        fi

        if [[ -f $1 ]]; then 
            echo "Restore file to table: '$0 restore-table'"
        fi
    else
        echo "USAGE: backup-info <path/to/backup/file/or/dir>"
        return 1
    fi
}

restore-db() {
    # Restore a previous backup of a specific database.

    if [[ -n $1 ]] && [[ -n $2 ]]; then
        bkdir=$1
        dbase=$2
        echo "Restoring backup $bkdir to ${dbase} ..."
        # Remove --clean to keep the existing db items.
        pg_restore  -v -U $POSTGRES_USER -p $POSTGRES_PORT \
                    --if-exists --clean -d ${dbase} $bkdir || exit 3
        echo "$bkdir Restored!"
        return 0
    else
        echo "USAGE: restore-db <path/to/directory> <db name>"
        return 2
    fi
}

restore-table() {
    # Restore a previous backup of a specific database table.

    if [[ -n $1 ]] && [[ -n $2 ]]; then
        cfile=$1
        dbase=$2
        echo "Restoring backup $cfile to ${dbase} ..."
        pg_restore  -v -U $POSTGRES_USER -p $POSTGRES_PORT \
                    --if-exists --clean -d ${dbase} $cfile || exit 3
        echo "$cfile Restored!"
        return 0
    else
        echo "USAGE: restore-table <path/to/file.pgdump> <db name>"
        return 2
    fi
}

echo "-- postgr.sh --"
function exit_script(){
    echo "Caught SIGTERM"
    stop
    exit 0
}

# Catch docker stop signal.
trap exit_script SIGTERM

if [[ "$#" -lt 1 ]]; then
    # If no argument is given, try starting the server.
    # This will fail if PGDATA was not persisted.
    run
    sleep infinity &
else
    # If arguments (e.g. install, run, create) are given, execute them.
    # These can be run by logging into the running container terminal.
    "$@"
fi

# Keep the container running by waiting for the sleep in bg.
wait
