FROM alpine
LABEL maintainer "carlos-el <celopez@correo.ugr.es>"

ARG PORT
ARG SERVICE

ENV PORT ${PORT}
ENV SERVICE ${SERVICE}

EXPOSE ${PORT}

COPY . /app
WORKDIR /app

RUN apk update && apk upgrade \     
    && apk add python3 \
    && pip3 install invoke \
    && invoke installDependencies

ENTRYPOINT invoke startServer -p ${PORT} -h 0.0.0.0 -s ${SERVICE}



