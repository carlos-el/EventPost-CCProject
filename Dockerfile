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
    && pip3 install falcon gunicorn

ENTRYPOINT gunicorn -b 0.0.0.0:${PORT} ${SERVICE} 



