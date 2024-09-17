import aioredis             #type: ignore
import json

redis = aioredis.from_url("redis://localhost")

async def publish(channel: str, message: dict):
    await redis.publish(channel, json.dumps(message))

async def subscribe(channel: str):
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)
    return pubsub
