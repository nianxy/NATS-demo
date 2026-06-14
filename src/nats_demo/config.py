from __future__ import annotations

import os
from dataclasses import dataclass


DEFAULT_BUCKET = "demo_kv"
DEFAULT_KEY = "demo.message"
DEFAULT_DOMAIN = "hub"
DEFAULT_CONTROL_SUBJECT = "control.leaf.command"
DEFAULT_CONTROL_COMMAND = "reload"
DEFAULT_RPC_SUBJECT = "rpc.leaf.status"


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


@dataclass(frozen=True)
class ControlConfig:
    nats_url: str
    subject: str
    command: str
    publish_interval: float


def load_control_config(default_url: str) -> ControlConfig:
    return ControlConfig(
        nats_url=os.getenv("NATS_URL", default_url),
        subject=os.getenv("CONTROL_SUBJECT", DEFAULT_CONTROL_SUBJECT),
        command=os.getenv("CONTROL_COMMAND", DEFAULT_CONTROL_COMMAND),
        publish_interval=float(os.getenv("PUBLISH_INTERVAL", "1.0")),
    )


@dataclass(frozen=True)
class RpcConfig:
    nats_url: str
    subject: str
    request_timeout: float
    publish_interval: float


def load_rpc_config(default_url: str) -> RpcConfig:
    return RpcConfig(
        nats_url=os.getenv("NATS_URL", default_url),
        subject=os.getenv("RPC_SUBJECT", DEFAULT_RPC_SUBJECT),
        request_timeout=float(os.getenv("REQUEST_TIMEOUT", "2.0")),
        publish_interval=float(os.getenv("PUBLISH_INTERVAL", "1.0")),
    )
