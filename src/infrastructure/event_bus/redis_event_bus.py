import redis
import json
import asyncio

from src.config import REDIS_HOST, REDIS_PORT
from src.core.applications.interfaces.event_bus import EventBus


class RedisEventBus(EventBus):
    def __init__(self, redis_host=REDIS_HOST, redis_port=REDIS_PORT):
        self.redis = redis.Redis(host=redis_host, port=redis_port)
        self.pubsub = self.redis.pubsub()
        self.handlers = {}

    async def publish(self, event):
        event_type = event.__class__.__name__
        message = {
            "event_type": event_type,
            "data": event.__dict__
        }

        await asyncio.to_thread(self.redis.publish, event_type, json.dumps(message))

    async def subscribe(self, event_type, handler):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        self.pubsub.subscribe(**{event_type: self._message_handler})

    def _message_handler(self, message):
        data = json.loads(message["data"])
        event_type = data["event_type"]
        event_data = data["data"]

        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                handler(event_type, event_data)

    async def listen(self):
        await asyncio.to_thread(self.pubsub.run_in_thread, daemon=True)