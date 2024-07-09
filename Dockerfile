FROM ubuntu:latest

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y python3 python3-pip
RUN apt upgrade python3-pip

WORKDIR /home

ENV PIP_BREAK_SYSTEM_PACKAGES=1

# layer to make successive builds quicker with dependency changes
RUN pip3 install pyspark==3.5.0
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src src
COPY data data

CMD python3 -m src.producer_service
