import json
import os
from confluent_kafka import Consumer, KafkaError
from data_lake_handler import DataLakeHandler
from delta_processor import DeltaProcessor

class Sourcing:
    def __init__(self, kafka_conf, mongo_conf):
        self.consumer = Consumer(kafka_conf)
        self.data_lake = DataLakeHandler(**mongo_conf)
        self.delta_processor = DeltaProcessor(self._map_to_delta(self.data_lake.get_all_active_listings()))

    def __del__(self):
        if self.consumer:
            self.consumer.close()

    def _map_to_delta(self, data):
        return [{'url': x['url'], 'reference': x['runId']} for x in data]

    def start_processing(self, ):
        self.consumer.subscribe(["jobsensei-sourcing-v1"])

        try:
            while True:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print(f'Reached end of partition {msg.partition()}')
                    else:
                        print(f'Error while consuming message: {msg.error()}')
                else:
                    self._process_message(msg=msg)
        except KeyboardInterrupt:
            pass

    def _process_message(self, msg):
        topic = msg.topic()
        value = msg.value()

        if topic == 'jobsensei-sourcing-v1':
            record = json.loads(value.decode())
            if self.delta_processor.is_new(record):
                self.data_lake.create_new_listing(record)

if __name__ == "__main__":
    kafka_conf = {
        'bootstrap.servers': 'kafka:9092', 
        'group.id': 'jobsensei-sourcing',
        'auto.offset.reset': 'earliest',    # Starts from beginning of topic, opposed to 'latest' which starts at the end
        'enable.auto.commit': True,         # Commit offset when message is successfully consumed
    }
    mongo_conf = {
        'user': os.environ.get("MONGO_USER"), 
        'password': os.environ.get("MONGO_PASSWORD"), 
        'server': os.environ.get("MONGO_SERVER"), 
        'db': os.environ.get("MONGO_DB")
    }

    sourcing = Sourcing(kafka_conf, mongo_conf)
    sourcing.start_processing()
