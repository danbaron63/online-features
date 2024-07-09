# Online Features Example
This repo contains sample code to implement streaming feature engineering from a local Kafka deployed using `docker compose`.

# Structure
This project contains 3 components:
1. Data producer
2. Kafka
3. Spark consumer

## Data Producer
The data producer is a simple python application that is deployed in a docker container. 
This will randomly sample records in `data/` and send them to Kafka.

## Kafka
This is deployed in a docker container with the necessary ports exposed.

## Spark consumer
This is a pyspark application that consumes data from Kafka and performs some transformations.
This can either be in streaming or batch mode.

# Installation
To install necessary python dependencies and build jars required by Spark, run:
```bash
make install
```
To activate your virtual environment, run:
```bash
source .venv/bin/activate
```

# Run
## Run Kafka
To run Kafka along with the random data producer run:
```bash
docker compose up --build -d
```
This will build and run the necessary containers.

## Run Spark
To run the Spark stream job run:
```bash
python -m src.consumer_spark
```
