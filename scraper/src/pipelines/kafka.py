# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from kafka import KafkaProducer


class KafkaPipeline:
    def process_item(self, item, spider):
        return item
