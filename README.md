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

# Feature Store
The [feature store](./demo/feature_repo) is available in `demo/feature_repo`.
[Feature definitions](./demo/feature_repo/transaction_repo.py) are defined in `transaction_repo.py` and a [test workflow](./demo/feature_repo/test_workflow.py) is available to test the feature store by requesting online features via the feature server and Feast SDK.

Note: to ensure data is available for the feature store, please run earlier steps and ensure the docker containers are up and running and the spark stream is running successfully. 
See [Run](#run) section for more details.

To setup the feature store, run:
```bash
cd demo/feature_repo
feast plan
feast apply
```

In order to populate the feature store, you must materialize the features from the offline store:
```bash
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
feast materialize-incremental $CURRENT_TIME
```

To start the feast server run:
```bash
feast serve
```

You can then run the test workflow:
```bash
python test_workflow.py
```