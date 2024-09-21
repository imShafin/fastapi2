import redis                    #type: ignore
from typing import Optional
from fastapi import HTTPException

class RedisClient:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.redis = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def set_cache(self, key: str, value: str, expiration: Optional[int] = None):
        try:
            self.redis.set(key, value, ex=expiration)
        except redis.RedisError as e:
            raise HTTPException(status_code=500, detail=f"Redis Error: {str(e)}")
    
    def get_cache(self, key: str) -> Optional[str]:
        try:
            value = self.redis.get(key)
            return value
        except redis.RedisError as e:
            raise HTTPException(status_code=500, detail=f"Redis Error: {str(e)}")

    def delete_cache(self, key: str):
        try:
            self.redis.delete(key)
        except redis.RedisError as e:
            raise HTTPException(status_code=500, detail=f"Redis Error: {str(e)}")

    def publish_message(self, channel: str, message: str):
        try:
            self.redis.publish(channel, message)
        except redis.RedisError as e:
            raise HTTPException(status_code=500, detail=f"Redis Error: {str(e)}")
    
    def subscribe_to_channel(self, channel: str):
        pubsub = self.redis.pubsub()
        try:
            pubsub.subscribe(channel)
            for message in pubsub.listen():
                if message and message['type'] == 'message':
                    yield message['data']
        except redis.RedisError as e:
            raise HTTPException(status_code=500, detail=f"Redis Error: {str(e)}")
