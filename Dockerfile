# base image
FROM python:3.8.0-alpine

RUN mkdir -p /usr/src/app/webservice

# set working directory
WORKDIR /usr/src/app/webservice

# add requirements (to leverage Docker cache)
COPY ./requirements.txt /usr/src/app/webservice/requirements.txt

RUN apk update && apk upgrade

# Needed for pyobdc (used by Windows SQL Driver)
RUN apk add --no-cache unixodbc-dev unixodbc g++

## Windows SQL driver
#Download the desired package(s)
RUN wget https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.6.1.1-1_amd64.apk
RUN wget https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.6.1.1-1_amd64.apk

#Install the package(s)
RUN apk add --no-cache --allow-untrusted msodbcsql17_17.6.1.1-1_amd64.apk
RUN apk add --no-cache --allow-untrusted mssql-tools_17.6.1.1-1_amd64.apk
##

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
 && pip3 install -r requirements.txt \
 && apk del .build-deps

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown appuser -R /usr/src/app/webservice
USER appuser