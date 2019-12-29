FROM bitnami/minideb
LABEL maintainer "carlos-el <celopez@correo.ugr.es>"

# Get the env_var PORT if set, if not set default value to 8080 
ENV PORT=8080

# Expose is only use to declare the internal port that is going to be
# used by the container. It might be useful for other developers, containers or apps.
EXPOSE ${PORT}

# Updates system, installs only compulsory dependencies
RUN apt update && apt upgrade && install_packages gnupg wget \
    # add mongo pgp key
    && wget --no-check-certificate -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add - \
    && echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.2 main" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list \
    && apt update \
    # install more dependencies
    && install_packages python3 python3-pip mongodb-org \
    && pip3 install falcon gunicorn pymongo falcon-caching \
    && useradd -m docker_user \
    # adds non-root user and creates directories for mongodb with the right permisssions.
    && mkdir -p /home/docker_user/mongodb/db /home/docker_user/mongodb/log \
    && chown -R docker_user:docker_user /home/docker_user/mongodb

# Sets default user to the new user created.
USER docker_user
# Copy app files to the container
COPY notifications_microservice /home/docker_user/notifications_microservice
# Sets the workdir to the new users workdir.
WORKDIR /home/docker_user

# Starts the app and starts mongo daemon in the back (--fork) and specifying log file and database folder.
CMD mongod --fork --logpath ~/mongodb/log/mongodb.log --dbpath ~/mongodb/db && gunicorn -w 7 -b 0.0.0.0:${PORT} notifications_microservice.app



