FROM        postgres:16

RUN         mkdir -p /postgres
WORKDIR     /postgres

RUN         groupadd -g 1000 pguser
RUN         useradd -l -m -u 1000 -g pguser pguser

EXPOSE      5454
ENV         POSTGRES_PORT=5454
ENV         TZ=America/New_York

#           Server manager script and config file.
COPY        postgr.sh /postgres/postgr.sh
COPY        postgresql.conf /postgres/_postgresql.conf
COPY        pg_hba.conf /postgres/_pg_hba.conf

#           Volume must be mounted at this location for persistence.
ENV         MNTVOL=/data
ENV         PGDATA=/data/PGDATA
RUN         mkdir -p $MNTVOL

#           Will catch this to stop the running server.
STOPSIGNAL  SIGTERM

RUN         chmod +x /postgres/postgr.sh
RUN         chown -R pguser /postgres
RUN         chown -R pguser $MNTVOL

USER        pguser
ENV         POSTGRES_USER=pguser

ENTRYPOINT  ["/bin/bash", "/postgres/postgr.sh"]


# USAGE:
# --------------------------------------------------------------------------
# First time setup of PGDATA:
# Step 1. Start the container.
# Step 2. Log into the running container. docker exec -it cont_name bash
# Step 3. Setup PGDATA using ./postgr.sh install
# Step 4. Start the server ./postgr.sh run
# Step 5. Create new database using ./postgr.sh create db_name
# Step 6. Restart and normally run the server/container.
# Step 7. Monitor the docker logs.
