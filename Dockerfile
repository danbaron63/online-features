FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt install -y python3 python3-pip
RUN apt upgrade python3-pip

WORKDIR /home

# layer to make successive builds quicker with dependency changes
RUN pip3 install pyspark==3.5.0 --break-system-packages
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --break-system-packages

# TODO: Fix this as when this layer is cached, code changes will not be detected
COPY src/* src/
COPY data/* data/

CMD python3 -m src.producer_service
