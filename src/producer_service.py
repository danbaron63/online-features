from confluent_kafka import Producer
from src.data_loader import get_random_record_json
import socket
import time
import logging
import os


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


host = os.environ.get("KAFKA_HOST", "localhost")
conf = {
    'bootstrap.servers': f'{host}:9094,{host}:9092',
    'client.id': socket.gethostname()}
logger.info("running with this config: %s", conf)

producer = Producer(conf)


# Produce a message
def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}]")


while True:
    try:
        rec = get_random_record_json("data/file1.csv")
        logger.debug("fetched record from producer: %s", rec)
        logger.info("writing record")
        producer.produce("account", key="key", value=rec, callback=delivery_report)
        time.sleep(1)
        producer.flush()
    except Exception as e:
        logger.error(str(e))
