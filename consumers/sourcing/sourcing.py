import json
import os
from confluent_kafka import Consumer, KafkaError, Producer
from data_lake_handler import DataLakeHandler
from delta_processor import DeltaProcessor
from topic import Topic

class Sourcing:
    def __init__(self, kafka_conf, mongo_conf):
        self.consumer = Consumer(kafka_conf)
        self.producer = Producer(kafka_conf)
        self.data_lake = DataLakeHandler(**mongo_conf)
        self.delta_processor = DeltaProcessor(self._map_all_to_delta(self.data_lake.get_all_active_listings()))

    def __del__(self):
        if self.consumer:
            self.consumer.close()

    def _map_all_to_delta(self, data):
        return [self._map_to_delta(x) for x in data]

    def _map_to_delta(self, record):
        return {'url': record['url'], 'reference': record['runId']}

    def start_processing(self, ):
        self.consumer.subscribe([Topic.SOURCING.value, Topic.END.value, Topic.NEW.value])

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
            print("Processing interrupted by user")
            pass
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
        finally:
            pass

    def _process_message(self, msg):
        topic = msg.topic()
        value = msg.value()
        record = json.loads(value.decode())

        if topic == Topic.SOURCING.value:
            if self.delta_processor.is_new(record):
                self._send_message(Topic.NEW.value, record)
        elif topic == Topic.NEW.value:
            self.data_lake.create_new_listing(record)

    def _send_message(self, topic, msg):
        try:
            self.producer.produce(topic, key=msg['runId'].encode('utf-8'), value=json.dumps(msg).encode('utf-8'))
        except Exception as e:
            print(f"Error: {str(e)}")

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
