# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from kafka import KafkaProducer
import json
import uuid
from datetime import datetime

class KafkaPipeline:
    def __init__(self, kafka_bootstrap_servers, start_topic, end_topic, sourcing_topic):
        self.start_topic = start_topic
        self.end_topic = end_topic
        self.sourcing_topic = sourcing_topic
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode("utf-8")
        )

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
        spider.run_id = str(uuid.uuid4())
        message = {"status": "start", "timestamp": datetime.now().isoformat(), "runId": spider.run_id}
        self.send_message(self.start_topic, message)

    def close_spider(self, spider):
        message = {"status": "end", "timestamp": datetime.now().isoformat(), "runId": spider.run_id}
        self.send_message(self.end_topic, message)
        self.producer.flush()
        self.producer.close()

    def process_item(self, item, spider):
        data = ItemAdapter(item)
        data["runId"] = spider.run_id
        self.send_message(self.sourcing_topic, data.asdict())
        return item

    def send_message(self, topic, message):
        try:
            self.producer.send(topic, message)
        except Exception as e:
            print("Error:", e)
