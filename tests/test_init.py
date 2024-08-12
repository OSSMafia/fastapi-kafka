from unittest.mock import AsyncMock

from main import SomeMessage
import pytest


def test_read_root(app_client):
    response = app_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


@pytest.mark.asyncio
async def test_consumer_subscriptions(app):
    assert await app.kafka_consumer.subscription() == frozenset(["test-topic", "test-topic-model"])


@pytest.mark.asyncio
async def test_consumer_message(app):
    mock_message = AsyncMock()
    mock_message.value = b'{"key": "value"}'
    handler = app.kafka_routes["test-topic"]
    result = await handler(mock_message)
    assert result == {"key": "value"}


@pytest.mark.asyncio
async def test_consumer_message_model(app):
    mock_message = AsyncMock()
    mock_message.value = b'{"test": "value"}'
    handler = app.kafka_routes["test-topic-model"]
    result = await handler(mock_message)
    assert isinstance(result, SomeMessage)


@pytest.mark.asyncio
async def test_consumer_message_validation(app):
    assert app.kafka_task is not None
    await app.stop_kafka_listener()
    assert app.kafka_task.cancelled() or app.kafka_task.done()
