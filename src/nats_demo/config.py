from __future__ import annotations

import os
from dataclasses import dataclass


DEFAULT_BUCKET = "demo_kv"
DEFAULT_KEY = "demo.message"
DEFAULT_DOMAIN = "hub"


@dataclass(frozen=True)
class AppConfig:
    nats_url: str
    js_domain: str
    bucket: str
    key: str
    publish_interval: float


def load_config(default_url: str) -> AppConfig:
    return AppConfig(
        nats_url=os.getenv("NATS_URL", default_url),
        js_domain=os.getenv("JS_DOMAIN", DEFAULT_DOMAIN),
        bucket=os.getenv("KV_BUCKET", DEFAULT_BUCKET),
        key=os.getenv("KV_KEY", DEFAULT_KEY),
        publish_interval=float(os.getenv("PUBLISH_INTERVAL", "1.0")),
    )
