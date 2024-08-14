# FastAPI Kafka

This package is a wrapper around the well-known [FastAPI](https://pypi.org/project/fastapi/) framework for introducing Kafka consumers as routes. No core FastAPI functionality has been altered and the documentation can be found [here](https://fastapi.tiangolo.com/).

Inspiration for this package comes from working on a NestJS API using [KafkaJS](https://docs.nestjs.com/microservices/kafka) where kafka consumer topics are defined as controllers. It's a very convenient pattern to work with.

New project so definitely more work to be done, contributions welcome.


## Installation

Install FastAPI Kafka with pip

```bash
  pip install fastapi_kafka
```
    
## Usage/Examples

Under the hood FastAPI Kafka uses [AIOKafka](https://github.com/aio-libs/aiokafka) to create a consumer. You define a consumer with the following, it matches the exact class inputs that [AIOKafkaConsumer](https://aiokafka.readthedocs.io/en/stable/api.html#aiokafka.AIOKafkaConsumer) uses:

```python
class KafkaConsumerConfig:
    loop: Optional[asyncio.AbstractEventLoop] = None
    bootstrap_servers: str = "localhost"
    client_id: Optional[str] = None
    group_id: Optional[str] = None
    group_instance_id: Optional[str] = None
    key_deserializer: Optional[Any] = None
    value_deserializer: Optional[Any] = None
    fetch_max_wait_ms: int = 500
    fetch_max_bytes: int = 52428800  # 50 MB
    fetch_min_bytes: int = 1
    max_partition_fetch_bytes: int = 1 * 1024 * 1024  # 1 MB
    request_timeout_ms: int = 40 * 1000  # 40 seconds
    retry_backoff_ms: int = 100
    auto_offset_reset: str = "latest"
    enable_auto_commit: bool = True
    auto_commit_interval_ms: int = 5000
    check_crcs: bool = True
    metadata_max_age_ms: int = 5 * 60 * 1000  # 5 minutes
    partition_assignment_strategy: tuple[Any, ...] = (RoundRobinPartitionAssignor,)
    max_poll_interval_ms: int = 300000  # 5 minutes
    rebalance_timeout_ms: Optional[int] = None
    session_timeout_ms: int = 10000  # 10 seconds
    heartbeat_interval_ms: int = 3000  # 3 seconds
    consumer_timeout_ms: int = 200  # 200 ms
    max_poll_records: Optional[int] = None
    ssl_context: Optional[ssl.SSLContext] = None
    security_protocol: str = "PLAINTEXT"
    api_version: str = "auto"
    exclude_internal_topics: bool = True
    connections_max_idle_ms: int = 540000  # 9 minutes
    isolation_level: str = "read_uncommitted"
    sasl_mechanism: str = "PLAIN"
    sasl_plain_password: Optional[str] = None
    sasl_plain_username: Optional[str] = None
    sasl_kerberos_service_name: str = "kafka"
    sasl_kerberos_domain_name: Optional[str] = None
    sasl_oauth_token_provider: Optional[Any] = None
```

---
### Simple Example

Here's a full example running a local kafka server:
```python
from typing import Any

from pydantic import BaseModel

from fastapi_kafka import FastAPIKafka
from fastapi_kafka.consumer import KafkaConsumerConfig


class SomeMessage(BaseModel):
    test: str


app = FastAPIKafka(
    kafka_consumer_config=KafkaConsumerConfig(
        bootstrap_servers="localhost:9092"
    )
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.consumer("test-topic")
async def read_item(item: Any):
    return item


@app.consumer("test-topic-model")
async def read_item_model(item: SomeMessage):
    return item
```

The FastAPIKafka can accept all standard constructor inputs as well.

To define a consumer topic you use `@app.consumer("<topic name>")`, you can define a kafka message as `Any` and it will return a UTF-8 decoded message when reading the `item`. 

If you use JSON messages you can define a pydantic model to read it much the same as a regular http route, the message will be transformed into an instance of that model.


### More Advanced Example (Using Upstash Kafka)
```python
from typing import Any
from uuid import uuid4

from pydantic import BaseModel

from fastapi_kafka import FastAPIKafka, create_ssl_context
from fastapi_kafka.consumer import KafkaConsumerConfig


class SomeMessage(BaseModel):
    test: str


consumer_config = KafkaConsumerConfig(
    bootstrap_servers='example-us1-kafka.upstash.io:9092',
    sasl_mechanism='SCRAM-SHA-256',
    security_protocol='SASL_SSL',
    ssl_context=create_ssl_context(),
    sasl_plain_username='xxx',
    sasl_plain_password='xxx',
    client_id=f'consumer-{uuid4()}',
    group_id='consumer-group-api',
    auto_offset_reset='earliest',
)

app = FastAPIKafka(kafka_consumer_config=consumer_config)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.consumer("test-topic")
async def read_item(item: Any):
    return item


@app.consumer("test-topic-model")
async def read_item_model(item: SomeMessage):
    return item

```

For `security_protocol` using `SASL_SSL` you must pass in a `create_ssl_context()`.

For even more advanced configuration such as defining your own certificates, more information can be found here: [AIOKafka SSL](https://aiokafka.readthedocs.io/en/stable/examples/ssl_consume_produce.html).

### FastAPI Lifespan

One material change that was made to FastAPI was how [Lifespan](https://fastapi.tiangolo.com/advanced/events/?h=lifespan) works. FastAPI Kafka initializes the Lifespan automatically to create the defined Kafka consumer, if you need additional start-up/shutdown behavior you can use the `startup_functions` or `shutdown_functions` when initializing the `FastAPIKafka` instance.

The `startup_functions` or `shutdown_functions` fields accept a list of synchronous or asynchronous functions to be executed before/after the yield in lifespan.

```python

async def my_startup_actions():
    await do_something()
    do_something_sync()

async def my_shutdown_actions():
    await do_something_on_shutdown()

app = FastAPIKafka(
    kafka_consumer_config=consumer_config,
    startup_functions=[my_startup_actions],
    shutdown_functions=[my_shutdown_actions]
)
```
## Acknowledgements

 Building upon the awesome [FastAPI](https://pypi.org/project/fastapi/) framework.
