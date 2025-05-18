import asyncio
from collections.abc import Awaitable
from contextlib import asynccontextmanager
from functools import wraps
from inspect import signature
import json
from typing import Callable
from typing import Optional
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import ValidationError

from fastapi_kafka.schema import KafkaConsumerConfig

LifecycleFunction = Union[Callable[[], None], Callable[[], Awaitable[None]]]


class FastAPIKafka(FastAPI):
    def __init__(
        self,
        kafka_consumer_config: KafkaConsumerConfig,
        startup_functions: Optional[list[LifecycleFunction]] = None,
        shutdown_functions: Optional[list[LifecycleFunction]] = None,
        *args,
        **kwargs,
    ):
        super().__init__(lifespan=self.lifespan, *args, **kwargs)
        self.kafka_consumer_config = kafka_consumer_config
        self.kafka_consumer = None
        self.kafka_routes = {}
        self.kafka_task = None
        self.startup_functions = startup_functions or []
        self.shutdown_functions = shutdown_functions or []

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        for func in self.startup_functions:
            if asyncio.iscoroutinefunction(func):
                await func()
            else:
                func()
        await self.start_kafka_listener()
        yield
        await self.stop_kafka_listener()
        for func in self.shutdown_functions:
            if asyncio.iscoroutinefunction(func):
                await func()
            else:
                func()

    def consumer(self, topic_name: str):
        def decorator(func):
            sig = signature(func)
            model = next((param.annotation for param in sig.parameters.values() if isinstance(param.annotation, type) and issubclass(param.annotation, BaseModel)), None)

            @wraps(func)
            async def wrapper(message, *args, **kwargs):
                message_value = message.value.decode("utf-8")

                if model:
                    try:
                        message_data = json.loads(message_value)
                        validated_message = model.model_validate(message_data)
                        return await func(validated_message, *args, **kwargs)
                    except (json.JSONDecodeError, ValidationError) as e:
                        raise ValueError(f"Kafka message validation error: {e}") from e
                else:
                    try:
                        message_data = json.loads(message_value)
                    except json.JSONDecodeError:
                        return await func(message_value, *args, **kwargs)
                    else:
                        return await func(message_data, *args, **kwargs)

            self.kafka_routes[topic_name] = wrapper
            return wrapper

        return decorator

    async def start_kafka_listener(self):
        self.kafka_task = asyncio.create_task(self.start_kafka_consumer())

    async def start_kafka_consumer(self):
        try:
            self.kafka_consumer = self.kafka_consumer_config.to_kafka_consumer(list(self.kafka_routes.keys()))
            await self.kafka_consumer.start()
        except Exception as e:
            raise Exception(f"Failed to start Kafka consumer: {e}") from e

        try:
            async for message in self.kafka_consumer:
                topic = message.topic
                handler = self.kafka_routes.get(topic)
                if handler:
                    await handler(message)
        except Exception as e:
            raise Exception(f"Failed to consume kafka message: {e}") from e
        finally:
            await self.kafka_consumer.stop()

    async def stop_kafka_listener(self):
        self.kafka_task.cancel()
        try:
            await self.kafka_task
        except asyncio.CancelledError:
            pass
