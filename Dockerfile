# base image
FROM python:3.7.0-alpine

RUN mkdir -p /usr/src/app/webservice

# set working directory
WORKDIR /usr/src/app/webservice

# add requirements (to leverage Docker cache)
COPY ./requirements.txt /usr/src/app/webservice/requirements.txt

# Needed for pyobdc (used by SQLAlchemy)
RUN apk add unixodbc unixodbc-dev freetds-dev freetds g++

# Needed for pyobdc
RUN echo $'[FreeTDS]\n\
Description = FreeTDS unixODBC Driver\n\
Driver = /usr/lib/libtdsodbc.so\n\
Setup = /usr/lib/libtdsodbc.so' >> /etc/odbcinst.ini

RUN echo $'[global]\n\
tds version = auto' >> ~/.freetds.conf

RUN apk add --virtual .build-deps gcc musl-dev \
 && pip3 install -r requirements.txt \
 && apk del .build-deps

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown appuser /usr/src/app/webservice
USER appuser