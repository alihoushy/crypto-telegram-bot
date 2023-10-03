from redis_package.redis_client import redis_client

def set_key_value(key, value):
    redis_client.set(key, value)

def get_key_value(key):
    return redis_client.get(key)

def incr_key(key):
    redis_client.incr(key)

def decr_key(key):
    redis_client.decr(key)
