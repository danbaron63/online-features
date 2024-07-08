from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': 'localhost:9094,localhost:9094',
        'client.id': socket.gethostname()}

producer = Producer(conf)

producer.produce("topic_a", key="key", value="value")

producer.flush()
