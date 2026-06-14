from __future__ import annotations

from nats.aio.client import Client
from nats.js import JetStreamContext
from nats.js.api import KeyValueConfig
from nats.js.errors import BucketNotFoundError


async def get_jetstream(nc: Client, domain: str) -> JetStreamContext:
    if domain:
        return nc.jetstream(domain=domain)
    return nc.jetstream()


async def ensure_bucket(js: JetStreamContext, bucket: str):
    try:
        return await js.key_value(bucket)
    except BucketNotFoundError:
        return await js.create_key_value(KeyValueConfig(bucket=bucket))
