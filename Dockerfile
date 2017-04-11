FROM ubuntu:14.04

MAINTAINER mudream "mudream4869@gmail.com"

RUN apt-get update && \
    apt-get install python3-pip nginx memcached -y

RUN pip3 install tornado python-memcached

RUN useradd imgcity && \
    printf imgcity\\nimgcity\\n | passwd && \
    mkdir /home/imgcity && \
    chown imgcity /home/imgcity
