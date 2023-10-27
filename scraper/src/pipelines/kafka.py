# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from confluent_kafka import Producer
import json
import uuid
from datetime import datetime

class KafkaPipeline:
    def __init__(self, kafka_bootstrap_servers, start_topic, end_topic, sourcing_topic):
        self.start_topic = start_topic
        self.end_topic = end_topic
        self.sourcing_topic = sourcing_topic
        conf = {
            'bootstrap.servers': kafka_bootstrap_servers,
            'client.id': 'jobsensei-scraper',
        }
        self.producer = Producer(**conf)

    @classmethod
    def from_crawler(cls, crawler):
        kafka_settings = crawler.settings.getdict("KAFKA_SETTINGS")
        return cls(
            kafka_settings.get("BOOTSTRAP_SERVERS"),
            kafka_settings.get("START_TOPIC"),
            kafka_settings.get("END_TOPIC"),
            kafka_settings.get("SOURCING_TOPIC")
        )

    def open_spider(self, spider): 
        self.run_id = str(uuid.uuid4())
        message = {"status": "start", "timestamp": datetime.now().isoformat(), "runId": self.run_id}
        self.send_message(self.start_topic, message)

    def close_spider(self, spider):
        message = {"status": "end", "timestamp": datetime.now().isoformat(), "runId": self.run_id}
        self.send_message(self.end_topic, message)
        self.producer.flush()

    def process_item(self, item, spider):
        data = ItemAdapter(item)
        data["runId"] = self.run_id
        self.send_message(self.sourcing_topic, data.asdict())
        return item

    def send_message(self, topic, message):
        try:
            self.producer.produce(topic, key=self.run_id.encode('utf-8'), value=json.dumps(message).encode('utf-8'))
        except Exception as e:
            print("Error:", e)
