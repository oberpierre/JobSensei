from pymongo import MongoClient
from confluent_kafka import Consumer, KafkaError
import json
import os
from urllib.parse import quote_plus

def connect_db(user, password, server):
    mongo_client = MongoClient('mongodb://%s:%s@%s/jobsensei' % (quote_plus(user), quote_plus(password), quote_plus(server)))
    db = mongo_client['jobsensei']
    listings_raw = db['listings_raw']
    return listings_raw

def process_message(msg, listings_raw):
    topic = msg.topic()
    value = msg.value()

    if topic == 'jobsensei-sourcing-v1':
        record = json.loads(value.decode())
        listings_raw.insert_one(record)

def consume_messages(listings_raw):
    conf = {
        'bootstrap.servers': 'kafka:9092', 
        'group.id': 'jobsensei-sourcing',
        'auto.offset.reset': 'earliest',    # Starts from beginning of topic, opposed to 'latest' which starts at the end
        'enable.auto.commit': True,         # Commit offset when message is successfully consumed
    }

    consumer = Consumer(conf)
    consumer.subscribe(["jobsensei-sourcing-v1"])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f'Reached end of partition {msg.partition()}')
                else:
                    print(f'Error while consuming message: {msg.error()}')
            else:
                process_message(listings_raw=listings_raw, msg=msg)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    mongo_user = os.environ.get("MONGO_USER")
    mongo_password = os.environ.get("MONGO_PASSWORD")
    mongo_server = os.environ.get("MONGO_SERVER")
    listings_raw = connect_db(user=mongo_user, password=mongo_password, server=mongo_server)
    consume_messages(listings_raw)