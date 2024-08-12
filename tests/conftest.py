from unittest.mock import AsyncMock
from unittest.mock import patch

from fastapi.testclient import TestClient
import pytest

from main import app as main_app


@pytest.fixture
def app():
    mock_kafka_consumer = AsyncMock()
    mock_kafka_consumer.subscription.return_value = frozenset(main_app.kafka_routes.keys())
    with patch("fastapi_kafka.schema.AIOKafkaConsumer", return_value=mock_kafka_consumer):
        with TestClient(main_app) as client:
            assert isinstance(client, TestClient)
            yield main_app


@pytest.fixture
def app_client():
    mock_kafka_consumer = AsyncMock()
    mock_kafka_consumer.subscription.return_value = frozenset(main_app.kafka_routes.keys())
    with patch("fastapi_kafka.schema.AIOKafkaConsumer", return_value=mock_kafka_consumer):
        with TestClient(main_app) as client:
            assert isinstance(client, TestClient)
            yield client
