FROM alpine
LABEL maintainer "carlos-el <celopez@correo.ugr.es>"

# Get the env_var PORT if set, if not set default value to 8080 
ENV PORT=8080

# Expose is only use to declare the internal port that is going to be
# used by the container. It might be useful for other developers, containers or apps.
EXPOSE ${PORT}

# Adds repositories needed for installing mongodb
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/main' >> /etc/apk/repositories \
    && echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/community' >> /etc/apk/repositories
# Updates system, installs only compulsory dependencies and creates non-root user.
RUN apk update && apk upgrade \     
    && apk add --no-cache python3 mongodb \
    && pip3 install falcon gunicorn pymongo \
    && adduser -D docker_user \
    && mkdir -p /home/docker_user/mongodb/db /home/docker_user/mongodb/log \
    && chown -R docker_user:docker_user /home/docker_user/mongodb

# Sets default user to the new user created.
USER docker_user
# Copy app files to the container
COPY events_microservice /home/docker_user/events_microservice
# Sets the workdir to the new users workdir.
WORKDIR /home/docker_user

# Starts the app and starts mongo daemon in the back (--fork) and specifying log file and database folder.
CMD mongod --fork --logpath ~/mongodb/log/mongodb.log --dbpath ~/mongodb/db && gunicorn -b 0.0.0.0:${PORT} events_microservice.app



