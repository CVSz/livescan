import asyncio
import json
from typing import Callable

from aiokafka import AIOKafkaConsumer

from livescan.utils.logging import build_logger

logger = build_logger("kafka-worker")


class KafkaEventConsumer:
    def __init__(self, bootstrap_servers: str, topic: str, group_id: str = "livescan"):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            enable_auto_commit=True,
        )

    async def run(self, handler: Callable[[dict], None]):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                try:
                    handler(msg.value)
                except Exception as exc:  # explicit stream safety
                    logger.error("stream_handler_failed", extra={"error": str(exc), "payload": msg.value})
        finally:
            await self.consumer.stop()


async def run_forever(worker: KafkaEventConsumer, handler: Callable[[dict], None]):
    while True:
        try:
            await worker.run(handler)
        except Exception as exc:
            logger.error("consumer_restart", extra={"error": str(exc)})
            await asyncio.sleep(2)
