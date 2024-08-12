from typing import Any

from pydantic import BaseModel

from fastapi_kafka import FastAPIKafka
from fastapi_kafka.consumer import KafkaConsumerConfig


class SomeMessage(BaseModel):
    test: str


app = FastAPIKafka(kafka_consumer_config=KafkaConsumerConfig(bootstrap_servers="localhost:9092"))


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.consumer("test-topic")
async def read_item(item: Any):
    return item


@app.consumer("test-topic-model")
async def read_item_model(item: SomeMessage):
    return item
