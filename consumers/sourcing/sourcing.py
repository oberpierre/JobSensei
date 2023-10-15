import json
import os
from confluent_kafka import Consumer, KafkaError, Producer
from data_lake_handler import DataLakeHandler
from delta_processor import DeltaProcessor
from topic import Topic
from state import State

class Sourcing:
    """Handles sourcing, processing, and messaging via Kafka topics."""

    def __init__(self, kafka_conf, mongo_conf):
        """Initializes the Kafka consumer, producer, DataLakeHandler, and DeltaProcessor with given configurations."""

        self.consumer = Consumer(kafka_conf)
        self.producer = Producer(kafka_conf)
        self.data_lake = DataLakeHandler(**mongo_conf)
        self.delta_processor = DeltaProcessor(self._map_all_to_delta(self.data_lake.get_all_active_listings()))

    def __del__(self):
        """Ensures the Kafka consumer is closed upon object destruction."""

        if self.consumer:
            self.consumer.close()

    def _map_all_to_delta(self, data):
        """Maps all records to the required fields for delta processing."""

        return [self._map_to_delta(x) for x in data]

    def _map_to_delta(self, record):
        """Maps a single record to required fields for delta processing."""

        return {'url': record['url'], 'reference': record['runId']}

    def start_processing(self):
        """Starts consuming messages from Kafka, processes them, and handles accordingly based on their topic."""

        self.consumer.subscribe([Topic.SOURCING.value, Topic.END.value, Topic.NEW.value, Topic.DELETE.value])

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
        """Processes a single Kafka message based on its topic and takes appropriate action."""

        topic = msg.topic()
        value = msg.value()
        record = json.loads(value.decode())

        if topic == Topic.SOURCING.value:
            state = self.delta_processor.insert_or_update(self._map_to_delta(record))
            if state == State.INSERTED:
                self._send_message(Topic.NEW.value, record)
        elif topic == Topic.NEW.value:
            self.data_lake.create_new_listing(record)
        elif topic == Topic.END.value:
            outdated_listings = self.delta_processor.get_outdated_ids(record['runId'])
            if outdated_listings:
                delete_message = {'urls': outdated_listings, 'timestamp': record['timestamp'], 'runId': record['runId']}
                self._send_message(Topic.DELETE.value, delete_message)
        elif topic == Topic.DELETE.value:
            self.data_lake.inactivate_listings(record['urls'])
            self.delta_processor.remove_data(record['urls'])

    def _send_message(self, topic, msg):
        """Sends the given message as JSON to a given Kafka topic."""
        
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
