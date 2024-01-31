import logging
import json
import os
from decouple import config
from confluent_kafka import Consumer, KafkaError, Producer
from data_lake_handler import DataLakeHandler
from delta_processor import DeltaProcessor
from topic import Topic
from state import State
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        if self.producer:
            self.producer.flush()

    def _map_all_to_delta(self, data):
        """Maps all records to the required fields for delta processing."""

        return [self._map_to_delta(x) for x in data]

    def _map_to_delta(self, record):
        """Maps a single record to required fields for delta processing."""

        return {'url': record['url'], 'reference': record['runId']}

    def _json_serialize(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("Object of type %s is not JSON serializable" % type(obj))

    def start_processing(self):
        """Starts consuming messages from Kafka, processes them, and handles accordingly based on their topic."""

        self.consumer.subscribe([
            Topic.SRC_SOURCING.value,
            Topic.SRC_END.value,
            Topic.SRC_NEW.value,
            Topic.SRC_DELETE.value,
            Topic.SRC_CATEGORIZED.value,
        ])

        try:
            while True:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.info(f'Reached end of partition {msg.partition()}')
                    else:
                        logger.error(f'Error while consuming message: {msg.error()}')
                else:
                    self._process_message(msg=msg)
        except KeyboardInterrupt:
            logger.info("Processing interrupted by user")
            pass
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
        finally:
            pass

    def _process_message(self, msg):
        """Processes a single Kafka message based on its topic and takes appropriate action."""

        topic = msg.topic()
        value = msg.value()
        record = json.loads(value.decode())

        logger.info(f"Received message with for topic {topic}: {record}")

        if topic == Topic.SRC_SOURCING.value:
            self._source_listing(record)
        elif topic == Topic.SRC_NEW.value:
            self._create_listing(record)
        elif topic == Topic.SRC_END.value:
            self._get_outdated_listings(record)
        elif topic == Topic.SRC_DELETE.value:
            self._inactivate_listing(record)
        elif topic == Topic.SRC_CATEGORIZED.value:
            self._create_categorized_listing(record)

    def _source_listing(self, record):
        state = self.delta_processor.insert_or_update(self._map_to_delta(record))
        if state == State.INSERTED:
            self._send_message(Topic.SRC_NEW, record)

    def _create_listing(self, record):
        uuid = self.data_lake.create_new_listing(record)
        record[uuid] = uuid
        logger.info(f"Job listing for URL {record['url']} has been created with UUID {record['uuid']}. Sending to LLM for categorization.")
        self._send_message(Topic.LLM_CATEGORIZE, {x:record[x] for x in record if x != '_id'})

    def _get_outdated_listings(self, record):
        outdated_listings = self.delta_processor.get_outdated_ids(record['runId'])
        if outdated_listings:
            delete_message = {'urls': outdated_listings, 'timestamp': record['timestamp'], 'runId': record['runId']}
            self._send_message(Topic.SRC_DELETE, delete_message)

    def _inactivate_listing(self, record):
        self.data_lake.inactivate_listings(record['urls'])
        self.delta_processor.remove_data(record['urls'])

    def _create_categorized_listing(self, record):
        self.data_lake.insert_categorization(record)

    def _send_message(self, topic, msg):
        """Sends the given message as JSON to a given Kafka topic."""
        
        key = msg['uuid'] if 'uuid' in msg else msg['runId']
        try:
            self.producer.produce(topic.value, key=key.encode('utf-8'), value=json.dumps(msg, default=self._json_serialize).encode('utf-8'))
        except Exception as e:
            logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    kafka_conf = {
        'bootstrap.servers': config('BOOTSTRAP_SERVERS', default='kafka:9092'), 
        'group.id': config('GROUP_ID', default='jobsensei-sourcing'),
        'auto.offset.reset': 'earliest',    # Starts from beginning of topic, opposed to 'latest' which starts at the end
        'enable.auto.commit': True,         # Commit offset when message is successfully consumed
    }
    mongo_conf = {
        'user': config('MONGO_USER', default=''), 
        'password': config('MONGO_PASSWORD', default=''), 
        'server': config('MONGO_SERVER', default='localhost:27017'), 
        'db': config('MONGO_DB', default='jobsensei')
    }

    sourcing = Sourcing(kafka_conf, mongo_conf)
    sourcing.start_processing()
