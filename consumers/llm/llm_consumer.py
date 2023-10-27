import sys
import logging
import json
from decouple import config
from llm import llm
from confluent_kafka import Consumer, KafkaError, Producer
from topic import Topic
from prompts import Prompts

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LlmConsumer:
  
    def __init__(self, kafka_conf, llm_args):
        self.llm_args = llm_args if llm_args else []
        self.consumer = Consumer(kafka_conf)
        self.producer = Producer(kafka_conf)

    def __del__(self):
        if self.consumer:
            self.consumer.close()
        if self.producer:
            self.producer.flush()

    def _extract_json(self, raw_text):
        start = raw_text.find('{')
        end = raw_text.rfind('}') + 1
        if start == -1 or end == 0:
            logging.error("No JSON found in the response.")
            return None

        json_str = raw_text[start:end]
        try:
            json_obj = json.loads(json_str)
            return json_obj
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON: {e}.")
        return None

    def _process_message(self, msg):
        topic = msg.topic()
        value = msg.value()
        record = json.loads(value.decode())

        logger.debug(f"Received message with topic {topic}: {record}")
        if topic == Topic.LLM_CATEGORIZE.value:
            prompt, prompt_args = Prompts.get_categorize_prompt(listing=record['content'])
            response = self._invoke_llm(prompt, prompt_args)
            res_json = self._extract_json(response)
            if res_json:
                logger.info(f"Response json: {res_json}")
                res_json['url'] = record['url']
                self._send_message(Topic.SRC_CATEGORIZED, record['url'], res_json)
            else:
                logger.error(f"Could not extract JSON from response: {response}")

    def _invoke_llm(self, prompt, prompt_args):
        args = [*self.llm_args, *(prompt_args if prompt_args else [])]
        logger.info(f"Invoking LLM with args {args} and prompt:\n{prompt}")
        return llm(prompt, *args)

    def _send_message(self, topic, key, msg):
        """Sends the given message as JSON to a given Kafka topic."""

        logger.info(f"Sending message {key}: {msg} for topic {topic.value}")

        try:
            self.producer.produce(topic.value, key=key, value=json.dumps(msg).encode('utf-8'))
            self.producer.flush()
        except Exception as e:
            logger.error(f"Error: {str(e)}")

    def start_processing(self):
        self.consumer.subscribe([Topic.LLM_CATEGORIZE.value])

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
                self._process_message(msg)

if __name__ == "__main__":
    kafka_conf = {
        'bootstrap.servers': config('BOOTSTRAP_SERVERS', default='kafka:9092'),
        'group.id': config('GROUP_ID', default='jobsensei-llm'),
        'max.poll.interval.ms': config('MAX_POLL_INVERVAL', default=1000000),
        'auto.offset.reset': 'earliest',    # Starts from beginning of topic, opposed to 'latest' which starts at the end
        'enable.auto.commit': True,         # Commit offset when message is successfully consumed
    }
    llm_args = sys.argv[1:]
    consumer = LlmConsumer(kafka_conf, llm_args)
    consumer.start_processing()