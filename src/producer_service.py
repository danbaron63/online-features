from confluent_kafka import Producer
from src.utils.data_loader import get_random_record
import json
import socket
import time
from datetime import datetime
import logging
import os


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


host = os.environ.get("KAFKA_HOST", "localhost")
conf = {
    'bootstrap.servers': f'{host}:9094,{host}:9092',
    'client.id': socket.gethostname(),
    'message.timeout.ms': '5000'
}
logger.info("running with this config: %s", conf)

producer = Producer(conf)


def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}]")


while True:
    try:
        rec = get_random_record("data/transactions/file1.csv")
        rec["timestamp"] = datetime.now().isoformat()
        logger.debug("fetched record from producer: %s", rec)
        logger.info("writing record")
        producer.produce("transactions", key=rec["id"], value=json.dumps(rec), callback=delivery_report)
        time.sleep(1)
        producer.flush()
    except Exception as e:
        logger.error(str(e))
