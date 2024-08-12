"""FastAPI framework with async Kafka integration"""

from aiokafka.helpers import create_ssl_context as create_ssl_context

from .consumer import FastAPIKafka as FastAPIKafka
from .schema import KafkaConsumerConfig as KafkaConsumerConfig
