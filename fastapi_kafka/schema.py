import asyncio
from dataclasses import dataclass
import ssl
from typing import Any
from typing import Optional

from aiokafka import AIOKafkaConsumer
from aiokafka.coordinator.assignors.roundrobin import RoundRobinPartitionAssignor


@dataclass
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

    def to_kafka_consumer(self, topics: list[str]) -> AIOKafkaConsumer:
        return AIOKafkaConsumer(
            *topics,
            loop=self.loop,
            bootstrap_servers=self.bootstrap_servers,
            client_id=self.client_id,
            group_id=self.group_id,
            group_instance_id=self.group_instance_id,
            key_deserializer=self.key_deserializer,
            value_deserializer=self.value_deserializer,
            fetch_max_wait_ms=self.fetch_max_wait_ms,
            fetch_max_bytes=self.fetch_max_bytes,
            fetch_min_bytes=self.fetch_min_bytes,
            max_partition_fetch_bytes=self.max_partition_fetch_bytes,
            request_timeout_ms=self.request_timeout_ms,
            retry_backoff_ms=self.retry_backoff_ms,
            auto_offset_reset=self.auto_offset_reset,
            enable_auto_commit=self.enable_auto_commit,
            auto_commit_interval_ms=self.auto_commit_interval_ms,
            check_crcs=self.check_crcs,
            metadata_max_age_ms=self.metadata_max_age_ms,
            partition_assignment_strategy=self.partition_assignment_strategy,
            max_poll_interval_ms=self.max_poll_interval_ms,
            rebalance_timeout_ms=self.rebalance_timeout_ms,
            session_timeout_ms=self.session_timeout_ms,
            heartbeat_interval_ms=self.heartbeat_interval_ms,
            consumer_timeout_ms=self.consumer_timeout_ms,
            max_poll_records=self.max_poll_records,
            ssl_context=self.ssl_context,
            security_protocol=self.security_protocol,
            api_version=self.api_version,
            exclude_internal_topics=self.exclude_internal_topics,
            connections_max_idle_ms=self.connections_max_idle_ms,
            isolation_level=self.isolation_level,
            sasl_mechanism=self.sasl_mechanism,
            sasl_plain_password=self.sasl_plain_password,
            sasl_plain_username=self.sasl_plain_username,
            sasl_kerberos_service_name=self.sasl_kerberos_service_name,
            sasl_kerberos_domain_name=self.sasl_kerberos_domain_name,
            sasl_oauth_token_provider=self.sasl_oauth_token_provider,
        )
