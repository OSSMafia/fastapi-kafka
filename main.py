from aiokafka.helpers import create_ssl_context
from uuid import uuid4
from typing import Any
from fastapi_kafka import FastAPIKafka
from fastapi_kafka.consumer import KafkaConsumerConfig
from logging import getLogger
import logging

logging.basicConfig(level=logging.INFO)
logger = getLogger(__name__)

consumer_config = KafkaConsumerConfig(
    bootstrap_servers='immense-lark-12967-us1-kafka.upstash.io:9092',
    sasl_mechanism='SCRAM-SHA-256',
    security_protocol='SASL_SSL',
    ssl_context=create_ssl_context(),
    sasl_plain_username='aW1tZW5zZS1sYXJrLTEyOTY3JBT-g8mrXB62OC82bc0WwOzk_QxfNGNa_IvL3IA',
    sasl_plain_password='OTU2YWE0OGYtMjJkZS00ZWNhLWI3YWUtZmY2OTIwMTA5Y2Ux',
    client_id=f'consumer-{uuid4()}',
    group_id='consumer-group-api',
    auto_offset_reset='earliest',
)

app = FastAPIKafka(kafka_consumer_config=consumer_config)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.consumer("camera-monitors")
async def read_item(item: Any):
    logger.info(item)
    return item


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)